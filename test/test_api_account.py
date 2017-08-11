#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from mymock import AbstractAccessorToTestData
from flask import Flask
from necco.api import AccountApi
from necco.config import ServerConfiguration
from necco.models import SqliteDb, AccountModel
import json
import unittest
from werkzeug.security import check_password_hash, generate_password_hash


class TestAccountApi(unittest.TestCase, AbstractAccessorToTestData):
    def get_db_path(self):
        """ Override AbstractAccessorToTestData.get_db_path().
        """
        return self._DB_PATH.format(self.__class__.__name__)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.initialize_db()

        self._db = SqliteDb(self.get_db_path())
        self._app = Flask("test")

        config = ServerConfiguration("")  # use default
        account_view = AccountApi.as_view("account", config=config, model=AccountModel(config, db=self._db))

        self._app.add_url_rule(rule="/api/account", view_func=account_view, methods=["POST", ])
        self._app.add_url_rule(rule="/api/account", view_func=account_view, methods=["GET", "PUT", "DELETE"], defaults={"user_id": None})
        self._app.add_url_rule(rule="/api/account/<int:user_id>", view_func=account_view, methods=["GET", "PUT", "DELETE"])

        self._app.config["SECRET_KEY"] = "key_for_test"
        self._app.config["TESTING"] = True

    def tearDown(self):
        self.remove_db_if_exists()

    def test_get(self):
        # session_transaction() is available instead of
        # patch.dict("necco.api.session", {"username": "taro.yamada@temp.com"}).
        # Patching session leads RuntimeError: Working outside of request context.
        #
        # http://flask.pocoo.org/docs/dev/testing/#accessing-and-modifying-sessions
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/account")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual("taro.yamada@temp.com", got_data.get("email"))
            self.assertEqual("山田", got_data.get("lastName"))
            self.assertEqual("太郎", got_data.get("firstName"))

    def test_get_with_valid_id(self):
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/account/1")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual("taro.yamada@temp.com", got_data.get("email"))
            self.assertEqual("山田", got_data.get("lastName"))
            self.assertEqual("太郎", got_data.get("firstName"))

            ret = c.get("/api/account/2")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual("jiro.yamada@temp.com", got_data.get("email"))
            self.assertEqual("山田", got_data.get("lastName"))
            self.assertEqual("次郎", got_data.get("firstName"))

    def test_get_with_invalid_id(self):
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/account/999")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual(None, got_data.get("email"))
            self.assertEqual(None, got_data.get("lastName"))
            self.assertEqual(None, got_data.get("firstName"))

    def test_put(self):
        with self._app.test_client() as c:
            user_id = 2

            with c.session_transaction() as sess:
                sess["user_id"] = user_id

            ret = c.put(
                "/api/account",
                data={
                    "email": "hoge@hoge.com",
                    "password_": "hoge's password",
                    "userId": str(user_id),
                    "lastName": "捕鯨",
                    "firstName": "穂芸",
                    "lastKanaName": "ほげい",
                    "firstKanaName": "ホゲイ",
                    "nickName": "ほげら",
                    "phoneNumber": "01-234-5678",
                    "faxNumber": "02-345-6789",
                    "prefectureId": "11", # 埼玉県
                    "address": "上尾市",
                    "streetAddress": "プリムヴェールシャンテ",
                    "latitude": "0.25",
                    "longitude": "0.5",
                    "profile": "趣味は機械学習モデル実装です",
                    # TODO: このへんもjs含めて実装
                    # "abilities": [
                    #     {
                    #         "id_": "",
                    #         "genre": "",
                    #         "detail": "",
                    #     },
                    # "requests": [
                    #     {
                    #         "id_": "",
                    #         "genre": "",
                    #         "detail": "",
                    #     },
                }
            )

            columns = [
                self._db.User.c.email,
                self._db.User.c.password_,
                self._db.Profile.c.userId,
                self._db.Profile.c.lastName,
                self._db.Profile.c.firstName,
                self._db.Profile.c.lastKanaName,
                self._db.Profile.c.firstKanaName,
                self._db.Profile.c.nickName,
                self._db.Profile.c.phoneNumber,
                self._db.Profile.c.faxNumber,
                self._db.Profile.c.prefectureId,
                self._db.Profile.c.address,
                self._db.Profile.c.streetAddress,
                self._db.Profile.c.latitude,
                self._db.Profile.c.longitude,
                self._db.Profile.c.profile,
            ]

            self.assertEqual(200, ret.status_code)

            joined = self._db.Profile.join(self._db.User, self._db.Profile.c.userId == self._db.User.c.id_)
            selected = joined.select(self._db.Profile.c.userId == user_id)

            result = selected.with_only_columns(columns).execute().fetchall()

            self.assertEqual(1, len(result))
            self.assertEqual("hoge@hoge.com", result[0][columns.index(self._db.User.c.email)])
            self.assertTrue(check_password_hash(result[0][columns.index(self._db.User.c.password_)], "hoge's password"))
            self.assertEqual(user_id, result[0][columns.index(self._db.Profile.c.userId)])
            self.assertEqual("捕鯨", result[0][columns.index(self._db.Profile.c.lastName)])
            self.assertEqual("穂芸", result[0][columns.index(self._db.Profile.c.firstName)])
            self.assertEqual("ほげい", result[0][columns.index(self._db.Profile.c.lastKanaName)])
            self.assertEqual("ホゲイ", result[0][columns.index(self._db.Profile.c.firstKanaName)])
            self.assertEqual("ほげら", result[0][columns.index(self._db.Profile.c.nickName)])
            self.assertEqual("01-234-5678", result[0][columns.index(self._db.Profile.c.phoneNumber)])
            self.assertEqual("02-345-6789", result[0][columns.index(self._db.Profile.c.faxNumber)])
            self.assertEqual(11, result[0][columns.index(self._db.Profile.c.prefectureId)])
            self.assertEqual("上尾市", result[0][columns.index(self._db.Profile.c.address)])
            self.assertEqual("プリムヴェールシャンテ", result[0][columns.index(self._db.Profile.c.streetAddress)])
            self.assertEqual(0.25, result[0][columns.index(self._db.Profile.c.latitude)])
            self.assertEqual(0.5, result[0][columns.index(self._db.Profile.c.longitude)])
            self.assertEqual("趣味は機械学習モデル実装です", result[0][columns.index(self._db.Profile.c.profile)])

    @unittest.skip
    def test_post_with_valid_params_by_normal_user(self):
        pass

    def test_post_with_valid_params_by_admin(self):
        with self._app.test_client() as c:

            # prepare
            user_id = 2  # admin user
            with c.session_transaction() as sess:
                sess["user_id"] = user_id

            email = "saburo@temp.com"
            password_ = "saburo's password"
            isAdmin = 1
            lastName = "山田"
            firstName = "三郎"
            lastKanaName = "やまだ"
            firstKanaName = "さぶろう"
            nickName = "さぶろー"
            phoneNumber = "01-234-5678"
            faxNumber = "02-345-6789"
            prefectureId = 11
            address = "上尾市"
            streetAddress = "プリムヴェールシャンテ"
            latitude = 0.25
            longitude = 0.5
            profile = "趣味は機械学習モデル実装です"

            # tested method
            ret = c.post(
                "/api/account",
                data={
                    "email": email,
                    "password_": password_,
                    "isAdmin": isAdmin,
                    "lastName": lastName,
                    "firstName": firstName,
                    "lastKanaName": lastKanaName,
                    "firstKanaName": firstKanaName,
                    "nickName": nickName,
                    "phoneNumber": phoneNumber,
                    "faxNumber": faxNumber,
                    "prefectureId": prefectureId,
                    "address": address,
                    "streetAddress": streetAddress,
                    "latitude": latitude,
                    "longitude": longitude,
                    "profile": profile,
                    # TODO: このへんもjs含めて実装
                    # "abilities": [
                    #     {
                    #         "id_": "",
                    #         "genre": "",
                    #         "detail": "",
                    #     },
                    # "requests": [
                    #     {
                    #         "id_": "",
                    #         "genre": "",
                    #         "detail": "",
                    #     },
                }
            )

            # verify
            self.assertEqual(200, ret.status_code)

            columns = [
                self._db.User.c.id_,
                self._db.User.c.email,
                self._db.User.c.password_,
                self._db.User.c.isAdmin,
                self._db.Profile.c.lastName,
                self._db.Profile.c.firstName,
                self._db.Profile.c.lastKanaName,
                self._db.Profile.c.firstKanaName,
                self._db.Profile.c.nickName,
                self._db.Profile.c.phoneNumber,
                self._db.Profile.c.faxNumber,
                self._db.Profile.c.prefectureId,
                self._db.Profile.c.address,
                self._db.Profile.c.streetAddress,
                self._db.Profile.c.latitude,
                self._db.Profile.c.longitude,
                self._db.Profile.c.profile,
            ]

            joined = self._db.Profile.join(self._db.User, self._db.Profile.c.userId == self._db.User.c.id_)
            selected = joined.select(self._db.User.c.email == email)
            result = selected.with_only_columns(columns).execute().fetchall()

            self.assertEqual(1, len(result))
            self.assertEqual(email, result[0][columns.index(self._db.User.c.email)])
            self.assertTrue(check_password_hash(result[0][columns.index(self._db.User.c.password_)], password_))
            self.assertEqual(user_id + 1, result[0][columns.index(self._db.Profile.c.userId)])  # auto increment
            self.assertEqual(lastName, result[0][columns.index(self._db.Profile.c.lastName)])
            self.assertEqual(firstName, result[0][columns.index(self._db.Profile.c.firstName)])
            self.assertEqual(lastKanaName, result[0][columns.index(self._db.Profile.c.lastKanaName)])
            self.assertEqual(firstKanaName, result[0][columns.index(self._db.Profile.c.firstKanaName)])
            self.assertEqual(nickName, result[0][columns.index(self._db.Profile.c.nickName)])
            self.assertEqual(phoneNumber, result[0][columns.index(self._db.Profile.c.phoneNumber)])
            self.assertEqual(faxNumber, result[0][columns.index(self._db.Profile.c.faxNumber)])
            self.assertEqual(prefectureId, result[0][columns.index(self._db.Profile.c.prefectureId)])
            self.assertEqual(address, result[0][columns.index(self._db.Profile.c.address)])
            self.assertEqual(streetAddress, result[0][columns.index(self._db.Profile.c.streetAddress)])
            self.assertEqual(latitude, result[0][columns.index(self._db.Profile.c.latitude)])
            self.assertEqual(longitude, result[0][columns.index(self._db.Profile.c.longitude)])
            self.assertEqual(profile, result[0][columns.index(self._db.Profile.c.profile)])

    @unittest.skip
    def test_post_with_invalid_params_by_admin(self):
        pass

    @unittest.skip("not implemented yet")
    def test_delete(self):
        pass

    @unittest.skip("not implemented yet")
    def test_delete_with_id_1(self):
        pass

    @unittest.skip("not implemented yet")
    def test_delete_with_id_2(self):
        pass

if __name__ == "__main__":
    unittest.main()

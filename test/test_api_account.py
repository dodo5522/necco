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
from necco.models import SqliteDb, AccountModel
import json
import os
import unittest
from unittest.mock import patch


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
        AccountApi.set_model(AccountModel(db=self._db))

        self._app = Flask("test")

        account_view = AccountApi.as_view("account")
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

    def test_get_with_id_1(self):
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/account/1")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual("taro.yamada@temp.com", got_data.get("email"))
            self.assertEqual("山田", got_data.get("lastName"))
            self.assertEqual("太郎", got_data.get("firstName"))

    def test_get_with_id_2(self):
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/account/2")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code)
            self.assertEqual("jiro.yamada@temp.com", got_data.get("email"))
            self.assertEqual("山田", got_data.get("lastName"))
            self.assertEqual("次郎", got_data.get("firstName"))

    @unittest.skip("not implemented yet")
    def test_post(self):
        with self._app.test_client() as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 2

            ret = c.post("/api/account", data={"name": "Saburo", "age": 12})

    def test_put(self):
        with self._app.test_client() as c:
            user_id = 2

            with c.session_transaction() as sess:
                sess["user_id"] = user_id

            ret = c.put(
                "/api/account",
                data={
                    "nickName": "JIRO",
                    "email": "jiro@for.test.com",
                }
            )

            self.assertEquals(200, ret.status_code, "invalid status_code: {}".format(ret.status_code))

            joined = self._db.Profile.join(self._db.User, self._db.Profile.c.userId == self._db.User.c.id_)
            selected = joined.select(self._db.Profile.c.userId == user_id)
            nick_name, email = selected.with_only_columns([self._db.Profile.c.nickName, self._db.User.c.email]).execute().fetchone()
            self.assertEquals("JIRO", nick_name)
            self.assertEquals("jiro@for.test.com", email)

    @unittest.skip("not implemented yet")
    def test_put_with_id_1(self):
        pass

    @unittest.skip("not implemented yet")
    def test_put_with_id_2(self):
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

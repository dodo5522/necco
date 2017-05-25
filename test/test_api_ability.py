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
import unittest
from flask import Flask
from necco.api import AbilityApi
from necco.models import SqliteDb, AbilityModel
import json


class TestAbilityApi(unittest.TestCase, AbstractAccessorToTestData):
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
        AbilityApi.set_model(AbilityModel(db=self._db))

        self._app = Flask("test")

        abilities_view = AbilityApi.as_view("abilities")
        self._app.add_url_rule(rule="/api/abilities", view_func=abilities_view, methods=["GET", ], defaults={"user_id": None})
        self._app.add_url_rule(rule="/api/abilities/<int:user_id>", view_func=abilities_view, methods=["GET", "PUT", "POST", "DELETE"])

        self._app.config["SECRET_KEY"] = "key_for_test"
        self._app.config["TESTING"] = True

    def tearDown(self):
        self.remove_db_if_exists()

    def test_get_all_users_abilities(self):
        # session_transaction() is available instead of
        # patch.dict("necco.api.session", {"username": "taro.yamada@temp.com"}).
        # Patching session leads RuntimeError: Working outside of request context.
        #
        # http://flask.pocoo.org/docs/dev/testing/#accessing-and-modifying-sessions
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/abilities")
            data = json.loads(ret.data.decode("utf-8"))

            self.assertEqual(200, ret.status_code)
            self.assertIn("length", data)
            self.assertIn("columns", data)
            self.assertIn("body", data)

            self.assertEqual(4, data.get("length"))
            self.assertEqual(6, len(data.get("columns")))
            self.assertIn("firstName", data.get("columns"))
            self.assertIn("lastName", data.get("columns"))
            self.assertIn("firstKanaName", data.get("columns"))
            self.assertIn("lastKanaName", data.get("columns"))
            self.assertIn("genre", data.get("columns"))
            self.assertIn("detail", data.get("columns"))
            self.assertEqual("太郎", data.get("body")[0].get("firstName"))
            self.assertEqual("太郎", data.get("body")[1].get("firstName"))
            self.assertEqual("太郎", data.get("body")[2].get("firstName"))
            self.assertEqual("次郎", data.get("body")[3].get("firstName"))
            self.assertEqual("植物の水やり", data.get("body")[0].get("detail"))
            self.assertEqual("子守り", data.get("body")[1].get("detail"))
            self.assertEqual("犬の散歩", data.get("body")[2].get("detail"))
            self.assertEqual("子守り", data.get("body")[3].get("detail"))
            self.assertEqual("", data.get("body")[0].get("genre"))
            self.assertEqual("", data.get("body")[1].get("genre"))
            self.assertEqual("", data.get("body")[2].get("genre"))
            self.assertEqual("", data.get("body")[3].get("genre"))

    def test_get_all_users_specified_columns_abilities(self):
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["user_id"] = 1

            ret = c.get("/api/abilities?firstName=takashi&detail")
            data = json.loads(ret.data.decode("utf-8"))

            self.assertEqual(200, ret.status_code)
            self.assertIn("length", data)
            self.assertIn("columns", data)
            self.assertIn("body", data)

            self.assertEqual(4, data.get("length"))
            self.assertEqual(2, len(data.get("columns")))
            self.assertIn("firstName", data.get("columns"))
            self.assertIn("detail", data.get("columns"))
            self.assertEqual("太郎", data.get("body")[0].get("firstName"))
            self.assertEqual("太郎", data.get("body")[1].get("firstName"))
            self.assertEqual("太郎", data.get("body")[2].get("firstName"))
            self.assertEqual("次郎", data.get("body")[3].get("firstName"))
            self.assertEqual("植物の水やり", data.get("body")[0].get("detail"))
            self.assertEqual("子守り", data.get("body")[1].get("detail"))
            self.assertEqual("犬の散歩", data.get("body")[2].get("detail"))
            self.assertEqual("子守り", data.get("body")[3].get("detail"))

    def test_get_a_users_abilities(self):
        with self._app.test_client() as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 2

            ret = c.get("/api/abilities/{}".format(1))  # 山田太郎のデータを取得
            data = json.loads(ret.data.decode("utf-8"))

            self.assertEqual(200, ret.status_code)
            self.assertIn("length", data)
            self.assertIn("columns", data)
            self.assertIn("body", data)

            self.assertEqual(3, data.get("length"))
            self.assertEqual(1, len(data.get("columns")))
            self.assertIn("genre", data.get("columns"))
            self.assertIn("detail", data.get("columns"))
            self.assertEqual("", data.get("body")[0].get("genre"))
            self.assertEqual("植物の水やり", data.get("body")[0].get("detail"))
            self.assertEqual("", data.get("body")[1].get("genre"))
            self.assertEqual("子守り", data.get("body")[1].get("detail"))
            self.assertEqual("", data.get("body")[2].get("genre"))
            self.assertEqual("犬の散歩", data.get("body")[2].get("detail"))

    def test_get_an_invalid_users_abilities(self):
        with self._app.test_client() as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

            ret = c.get("/api/abilities/{}".format(0xffffffffffffffffffffffffffffffff))
            data = json.loads(ret.data.decode("utf-8"))

            self.assertEqual(200, ret.status_code)
            self.assertIn("length", data)
            self.assertIn("columns", data)
            self.assertIn("body", data)

            self.assertEqual(3, data.get("length"))
            self.assertEqual(1, len(data.get("columns")))
            self.assertIn("genre", data.get("columns"))
            self.assertIn("detail", data.get("columns"))
            self.assertEqual("", data.get("body")[0].get("genre"))
            self.assertEqual("植物の水やり", data.get("body")[0].get("detail"))
            self.assertEqual("", data.get("body")[1].get("genre"))
            self.assertEqual("子守り", data.get("body")[1].get("detail"))
            self.assertEqual("", data.get("body")[2].get("genre"))
            self.assertEqual("犬の散歩", data.get("body")[2].get("detail"))

    def test_put_to_update_a_users_ability(self):
        test_user_id = 1

        with self._app.test_client() as c:
            with c.session_transaction() as sess:
                sess["user_id"] = test_user_id

            ret = c.get("/api/abilities/{}".format(test_user_id))

    def test_put_to_update_a_users_abilities(self):
        pass

    def test_post_to_create_a_users_abilities(self):
        pass

    def test_delete_a_users_ability(self):
        pass


if __name__ == "__main__":
    unittest.main()

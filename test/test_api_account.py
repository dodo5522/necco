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

import unittest
from unittest.mock import patch
from flask import Flask
from necco.api import AccountApi
from necco.models import SqliteDb, AccountModel
import json
import sys
# import subprocess as sub
# import tempfile


class TestAccountApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._db_path = "/tmp/necco_test.db"

    @classmethod
    def tearDownClass(cls):
        if 0:
            sys.remove(cls._db_path)

    def setUp(self):
        AccountApi.set_model(AccountModel(db=SqliteDb(self._db_path)))

        self._app = Flask("test")
        self._app.add_url_rule(
            rule="/api/account",
            view_func=AccountApi.as_view("account"))

        self._app.config["SECRET_KEY"] = "key_for_test"
        self._app.config["TESTING"] = True

    def tearDown(self):
        delattr(self, "_app")

    def test_get(self):
        # session_transaction() is available instead of
        # patch.dict("necco.api.session", {"username": "taro.yamada@temp.com"}).
        # Patching session leads RuntimeError: Working outside of request context.
        #
        # http://flask.pocoo.org/docs/dev/testing/#accessing-and-modifying-sessions
        with self._app.test_client() as c:
            with c.session_transaction() as ses:
                ses["username"] = "taro.yamada@temp.com"

            ret = c.get("/api/account")
            got_data = json.loads(ret.data.decode("utf8"))

            self.assertEqual(200, ret.status_code, "invalid status_code")
            self.assertEqual(got_data["email"], "taro.yamada@temp.com", "invalid email")
            self.assertEqual(got_data["phoneNumber"], "010-010-010", "invalid phone number")
            self.assertEqual(got_data["faxNumber"], "101-101-101", "invalid fax number")

    def test_post(self):
        pass


if __name__ == "__main__":
    unittest.main()

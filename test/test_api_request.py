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
from necco.api import RequestApi
from necco.models import SqliteDb, RequestModel
import json
import os
import sys
import unittest
from unittest.mock import patch


class TestRequestApi(unittest.TestCase, AbstractAccessorToTestData):
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
        RequestApi.set_model(RequestModel(db=self._db))

        self._app = Flask("test")
        self._app.add_url_rule(
            rule="/api/request",
            view_func=RequestApi.as_view("request"))

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
                ses["username"] = "taro.yamada@temp.com"

            ret = c.get("/api/request")
            print(ret)

    def test_post(self):
        pass


if __name__ == "__main__":
    unittest.main()

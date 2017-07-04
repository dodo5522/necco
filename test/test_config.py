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

import configparser
from glob import glob
import inspect
import unittest
from necco.config import ServerConfiguration
import os


_CONFIG_FILE_HEADER = "/tmp/test_config"

_CONFIG_FILE_VALID_CONTENT = """
[GENERAL]
title = 地域通貨ねっこ通帳
docroot = /var/lib/necco/templates
secret_key = abcdefghijklmnopqrstuvwxyz1234567890

[SQL]
db = necco
port = 3306
server = localhost
user = necco_manager
password = necco_manager_password
"""


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        for fn in glob("{}*".format(_CONFIG_FILE_HEADER)):
            os.remove(fn)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_with_no_configuration_file(self):
        config_file = "{}_{}.ini".format(
            _CONFIG_FILE_HEADER,
            inspect.currentframe().f_code.co_name)

        if os.path.exists(config_file):
            os.remove(config_file)

        config = ServerConfiguration(config_file)

        self.assertEqual("Title", getattr(config, "TITLE"))
        self.assertEqual("/var/tmp/necco", getattr(config, "DOCROOT"))
        self.assertEqual("necco_temporary_key", getattr(config, "SECRET_KEY"))
        self.assertEqual("necco", getattr(config, "SQL_DB"))
        self.assertEqual(3306, getattr(config, "SQL_PORT"))
        self.assertEqual("localhost", getattr(config, "SQL_SERVER"))
        self.assertEqual("guest", getattr(config, "SQL_USER"))
        self.assertEqual("guest's password", getattr(config, "SQL_PASSWORD"))

    def test_with_valid_configuration_file(self):
        config_file = "{}_{}.ini".format(
            _CONFIG_FILE_HEADER,
            inspect.currentframe().f_code.co_name)

        with open(config_file, "w") as f:
            f.write(_CONFIG_FILE_VALID_CONTENT)

        config = ServerConfiguration(config_file)

        self.assertEqual("地域通貨ねっこ通帳", getattr(config, "TITLE"))
        self.assertEqual("/var/lib/necco/templates", getattr(config, "DOCROOT"))
        self.assertEqual("abcdefghijklmnopqrstuvwxyz1234567890", getattr(config, "SECRET_KEY"))
        self.assertEqual("necco", getattr(config, "SQL_DB"))
        self.assertEqual(3306, getattr(config, "SQL_PORT"))
        self.assertEqual("localhost", getattr(config, "SQL_SERVER"))
        self.assertEqual("necco_manager", getattr(config, "SQL_USER"))
        self.assertEqual("necco_manager_password", getattr(config, "SQL_PASSWORD"))

    def test_with_invalid_configuration_file(self):
        config_file = "{}_{}.ini".format(
            _CONFIG_FILE_HEADER,
            inspect.currentframe().f_code.co_name)

        with open(config_file, "w") as f:
            f.write("docroot = /var/lib/necco/templates")

        self.assertRaises(configparser.MissingSectionHeaderError, ServerConfiguration, config_file)


if __name__ == "__main__":
    unittest.main()

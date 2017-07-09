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
import os


class ServerConfiguration(object):
    _DEFAULTS = {
        "GENERAL": {
            "TITLE": "Title",
            "DOCROOT": "/var/tmp/necco",
            "SECRET_KEY": "necco_temporary_key",
        },
        "SQL": {
            "DB": "necco",
            "PORT": "3306",
            "SERVER": "localhost",
            "USER": "guest",
            "PASSWORD": "guest's password",
        },
    }

    def __init__(self, file_path):
        """ Set configuration based on the specified file.

        arguments:
            file_path: path to file or file like object.
        """
        def get_default_parser():
            parser = configparser.ConfigParser()

            for section in self._DEFAULTS.keys():
                parser.add_section(section)

                for option in self._DEFAULTS.get(section).keys():
                    parser.set(section, option, self._DEFAULTS.get(section).get(option))

            return parser

        if isinstance(file_path, str):
            if os.path.exists(file_path):
                parser = configparser.ConfigParser()
                parser.read(file_path, encoding="UTF-8")
            else:
                parser = get_default_parser()
        else:
            parser = configparser.ConfigParser()
            parser.read_file(file_path)

        self.TITLE = parser["GENERAL"]["TITLE"]
        self.DOCROOT = parser["GENERAL"]["DOCROOT"]
        self.SECRET_KEY = parser["GENERAL"]["SECRET_KEY"]
        self.SQL_DB = parser["SQL"]["DB"]
        self.SQL_PORT = int(parser["SQL"]["PORT"])
        self.SQL_SERVER = parser["SQL"]["SERVER"]
        self.SQL_USER = parser["SQL"]["USER"]
        self.SQL_PASSWORD = parser["SQL"]["PASSWORD"]

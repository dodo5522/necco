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
        "MYSQL": {
            "DB": "necco",
            "PORT": "3306",
            "SERVER": "localhost",
            "USER": "guest",
            "PASSWORD": "guest's password",
        },
    }

    def __init__(self, file_path="/etc/necco/necco.ini"):
        """ Set configuration based on the specified file.

        returns:
            Default configuration data dict.
        raises:
            PermissionError: If configuration file cannot be written on the specified path.
        """
        def get_default_parser():
            parser = configparser.ConfigParser()

            for section in self._DEFAULTS.keys():
                parser.add_section(section)

                for option in self._DEFAULTS.get(section).keys():
                    parser.set(section, option, self._DEFAULTS.get(section).get(option))

            return parser

        if os.path.exists(file_path):
            parser = configparser.ConfigParser()
            parser.read(file_path, encoding="UTF-8")
        else:
            parser = get_default_parser()
            try:
                with open(file_path, "w") as f:
                    parser.write(f)
            except PermissionError as e:
                pass
            except Exception as e:
                # TODO: logging or something
                raise

        self.TITLE = parser["GENERAL"]["TITLE"]
        self.DOCROOT = parser["GENERAL"]["DOCROOT"]
        self.SECRET_KEY = parser["GENERAL"]["SECRET_KEY"]
        self.MYSQL_DB = parser["MYSQL"]["DB"]
        self.MYSQL_PORT = int(parser["MYSQL"]["PORT"])
        self.MYSQL_SERVER = parser["MYSQL"]["SERVER"]
        self.MYSQL_USER = parser["MYSQL"]["USER"]
        self.MYSQL_PASSWORD = parser["MYSQL"]["PASSWORD"]

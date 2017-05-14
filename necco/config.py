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

_INIT = "/etc/necco/necco.ini"

_parser = configparser.ConfigParser()
_parser.read(_INIT, encoding="UTF-8")

# section_general = _parser.get("GENERAL")
# section_general.get("", )

if len(_parser.sections()) is not 0:
    TITLE = _parser["GENERAL"]["TITLE"]
    DOCROOT = _parser["GENERAL"]["DOCROOT"]
    SECRET_KEY = _parser["GENERAL"]["SECRET_KEY"]
    MYSQL_DB = _parser["MYSQL"]["DB"]
    MYSQL_PORT = int(_parser["MYSQL"]["PORT"])
    MYSQL_SERVER = _parser["MYSQL"]["SERVER"]
    MYSQL_USER = _parser["MYSQL"]["USER"]
    MYSQL_PASSWORD = _parser["MYSQL"]["PASSWORD"]
else:
    _parser["GENERAL"] = {}
    TITLE = _parser["GENERAL"]["TITLE"] = "Title"
    DOCROOT = _parser["GENERAL"]["DOCROOT"] = "/var/tmp/necco"
    SECRET_KEY = _parser["GENERAL"]["SECRET_KEY"] = "necco_temprary_key"

    _parser["MYSQL"] = {}
    MYSQL_DB = _parser["MYSQL"]["DB"] = "necco"
    MYSQL_PORT = _parser["MYSQL"]["PORT"] = "3306"
    MYSQL_SERVER = _parser["MYSQL"]["SERVER"] = "localhost"
    MYSQL_USER = _parser["MYSQL"]["USER"] = "guest"
    MYSQL_PASSWORD = _parser["MYSQL"]["PASSWORD"] = "guest's password"

    with open(_INIT, "w") as c:
        _parser.write(c)

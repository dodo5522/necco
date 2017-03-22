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

from necco.models import db
from werkzeug.security import check_password_hash


class AbstractAuthentication(object):
    def __init__(self, id_, password):
        self._is_authenticated = self._do_authentication(id_, password)

    def _do_authentication(self, id_, password):
        raise NotImplementedError

    def is_authenticated(self):
        return self._is_authenticated


class PasswordAuthantication(AbstractAuthentication):
    def __init(self, id_, password, db=db):
        super().__init__(id_, password)
        self._db = db

    def _do_authentication(self, id_, password):
        # FIXME: move this sentence to db.py as some API.
        record = db.execute("SELECT email, password_ FROM User WHERE email = '{}'".format(id_))

        if not record:
            return False

        _, hashed_password = record[0]

        if not check_password_hash(hashed_password, password):
            return False

        return True

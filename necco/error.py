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


class NoAdminPermission(Exception):
    status_code = 403  # fobidden

    def __init__(self, message="You don't have admin permission.", status_code=None, payload=None):
        Exception.__init__(self)

        self._message = message

        if status_code is not None:
            self._status_code = status_code

        self._payload = payload

    def to_dict(self):
        ret = dict(self.payload or ())
        ret["message"] = self._message
        return ret

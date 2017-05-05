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

from necco.models import AccountModel
from werkzeug.security import check_password_hash


class AbstractAuthentication(object):
    def __init__(self, email, password):
        self._is_authenticated = False
        self._authenticated_user_id = None

        try:
            self._is_authenticated = self._do_authentication(email, password)
            self._authenticated_user_id = self._get_user_id(email)
        except (ValueError, TypeError) as e:
            pass
        except:
            raise

    def _do_authentication(self, email, password):
        raise NotImplementedError

    def _get_user_id(self):
        raise NotImplementedError

    def is_authenticated(self):
        return self._is_authenticated

    def get_authenticated_user_id(self):
        return self._authenticated_user_id if self._is_authenticated else None


class PasswordAuthentication(AbstractAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _do_authentication(self, email, password):
        if not check_password_hash(
                AccountModel().get_hashed_password(self._get_user_id(email)),
                password):
            return False

        return True

    def _get_user_id(self, email):
        return AccountModel().get_id(email)

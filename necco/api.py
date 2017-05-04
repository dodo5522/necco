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

import json
from flask import session, request
from flask.views import MethodView
from necco.models import AccountModel, AbilityModel, RequestModel, PrefectureModel


class ModelSwitcher(object):
    _model = None

    @classmethod
    def set_model(cls, model):
        cls._model = model

    @classmethod
    def is_model_set(cls):
        return cls._model is not None



class AbilityApi(MethodView, ModelSwitcher):
    """ for route of /api/abilities """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_model_set():
            self.set_model(AbilityModel())

    def get(self):
        try:
            columns = request.args if request.args else self._model.get_columns()
            abilities = [{columns[i]: r[i] for i in range(len(columns))} for r in self._model.yield_record()]
        except:
            columns = abilities = []

        sending_obj = {
            "length": len(abilities),
            "columns": columns,
            "body": abilities
        }

        return json.dumps(sending_obj)

    def post(self):
        return "<html><body>Not implemented yet.</body></html>"


class RequestApi(MethodView, ModelSwitcher):
    """ for route of /api/requests """

    def __init__(self, *args, **kwargs):
        super(RequestApi, self).__init__(*args, **kwargs)
        if not self.is_model_set():
            self.set_model(RequestModel())

    def get(self):
        try:
            columns = request.args if request.args else self._model.get_columns()
            requests = [{columns[i]: r[i] for i in range(len(columns))} for r in self._model.yield_record()]
        except:
            columns = requests = []

        sending_obj = {
            "length": len(requests),
            "columns": columns,
            "body": requests
        }

        return json.dumps(sending_obj)

    def post(self):
        return "<html><body>Not implemented yet.</body></html>"


class PrefectureApi(MethodView, ModelSwitcher):
    """ for route of /api/prefs """

    def __init__(self, *args, **kwargs):
        super(PrefectureApi, self).__init__(*args, **kwargs)
        if not self.is_model_set():
            self.set_model(PrefectureModel())

    def get(self):
        columns = ["id", "name"]
        prefs = [{columns[i]: r[i] for i in range(len(columns))} for r in self._model.yield_record()]

        sending_obj = {
            "length": len(prefs),
            "body": prefs
        }

        return json.dumps(sending_obj)


class AccountApi(MethodView, ModelSwitcher):
    """ for route of "/api/account" """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_model_set():
            self.set_model(AccountModel())

    def post(self):
        """ Create new user account. """

        got = {key: value for key, value in request.form.items()}

        # create account data via AccountModel

        return json.dumps(got)

    def get(self, user_id):
        """ Get user account information who logs in currently. """

        try:
            email = self._model.get_email(user_id) if user_id else session["username"]
            user_info = self._model.get_all(email)
        except Exception:
            user_info = {}

        return json.dumps(user_info)

    def put(self, user_id):
        """ Update information for the current user account. """

        got = {key: value for key, value in request.form.items()}

        # create account data via AccountModel

        return json.dumps(got)

    def delete(self, user_id):
        """ Delete the specified user account. """

        return "Not implemented yet"

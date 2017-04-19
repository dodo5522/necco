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
from necco.models import Database


_db = Database()


class AbilityApi(MethodView):
    """ for route of /api/abilities """

    def get(self):
        args = request.args

        if args:
            columns = args
        else:
            columns = ["name", "kana", "detail"]

        abilities = [{columns[i]: r[i] for i in range(len(columns))} for r in _db.yield_abilities()]

        sending_obj = {
            "length": len(abilities),
            "body": abilities
        }

        return json.dumps(sending_obj)

    def post(self):
        return "<html><body>Not implemented yet.</body></html>"


class RequestApi(MethodView):
    """ for route of /api/requests """

    def get(self):
        columns = ["name", "kana", "detail"]
        requests = [{columns[i]: r[i] for i in range(len(columns))} for r in _db.yield_requests()]

        sending_obj = {
            "length": len(requests),
            "body": requests
        }

        return json.dumps(sending_obj)

    def post(self):
        return "<html><body>Not implemented yet.</body></html>"


class PrefectureApi(MethodView):
    """ for route of /api/prefs """

    def get(self):
        columns = ["id", "name"]
        prefs = [{columns[i]: r[i] for i in range(len(columns))} for r in _db.yield_prefectures()]

        sending_obj = {
            "length": len(prefs),
            "body": prefs
        }

        return json.dumps(sending_obj)


class AccountApi(MethodView):
    """ for route of "/api/account" """

    def get(self):
        email = session["username"]
        user_info = _db.get_user_account(email)
        return json.dumps(user_info)

    def post():
        got = {key: item for key, item in request.form.items()}
        return json.dumps(got)

    def put():
        return "Not implemented yet"

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
from necco.auth import PasswordAuthentication
from flask import render_template, session, request, redirect
from flask.views import View, MethodView


class LoginView(MethodView):

    def __init__(self, *args, **kwargs):
        self._config = kwargs.pop("config")
        super(MethodView, self).__init__(*args, **kwargs)

    def get(self):
        return render_template(
            "login.html",
            title=self._config.TITLE)

    def post(self):
        auth = PasswordAuthentication(
            request.form["email"],
            request.form["password"],
            config=self._config)

        if not auth.is_authenticated():
            return redirect("/login")

        session["user_id"] = auth.get_authenticated_user_id()
        return redirect("/")


class LogoutView(MethodView):
    def get(self):
        session.pop("user_id", None)
        return redirect("/login")


class MainView(View):
    methods = ["GET", ]

    def __init__(self, *args, **kwargs):
        self._config = kwargs.pop("config")
        super(View, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        if not session["user_id"]:
            return redirect("/login")

        # FIXME: Dummy data. Remove it if data can be got from SQL DB.
        records = [
            {
                "dealed_at": "2017-03-10",
                "from_whom": "りん",
                "to_whom": "",
                "what": "イースト菌の育て方",
                "price_necco": -1,
                "price_yen": -100,
            },
            {
                "dealed_at": "2017-03-13",
                "from_whom": "",
                "to_whom": "さき",
                "what": "電子回路修理",
                "price_necco": 1,
                "price_yen": 0,
            },
        ]

        return render_template(
            "index.html",
            title=self._config.TITLE,
            username=session["user_id"],
            records=records)


class DebugView(MethodView):
    """ for route of /temp """

    def get(self):
        return json.dumps(request.args)

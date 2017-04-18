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
from necco import config
from necco.auth import PasswordAuthentication
from flask import render_template, session, request, redirect
from flask.views import View, MethodView


class LoginView(MethodView):
    def get(self):
        return render_template(
            "login.html",
            title=config.TITLE)

    def post(self):
        auth = PasswordAuthentication(
            request.form["email"],
            request.form["password"])

        if not auth.is_authenticated():
            return redirect("/login")

        session["username"] = request.form["email"]
        return redirect("/")


class LogoutView(MethodView):
    def get(self):
        session.pop("username", None)
        return redirect("/login")


class MainView(View):
    methods = ["GET", ]

    def dispatch_request(self):
        if not session["username"]:
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
            title=config.TITLE,
            username=session["username"],
            records=records)


#class ApiView(View):
#    def __init__(self, app=None, db=None, *args, **kwargs):
#        super(ApiView, self).__init__(app=app)
#        self._db = db
#        app.add_url_rule(rule="/api", view_func=self.as_view(""))
#
#    def get_abilities(self):
#        columns = ["name", "kana", "detail"]
#        abilities = [{columns[i]: r[i] for i in range(len(columns))} for r in self.db.yield_abilities()]
#
#        sending_obj = {
#            "length": len(abilities),
#            "body": abilities
#        }
#
#        return json.dumps(sending_obj)
#
#    @_app.route("/api/requests", methods=["GET", ])
#    def get_requests(self):
#        columns = ["name", "kana", "detail"]
#        requests = [{columns[i]: r[i] for i in range(len(columns))} for r in self.db.yield_requests()]
#
#        sending_obj = {
#            "length": len(requests),
#            "body": requests
#        }
#
#        return json.dumps(sending_obj)
#
#    @_app.route("/api/prefs", methods=["GET", ])
#    def get_prefectures(self):
#        columns = ["id", "name"]
#        prefs = [{columns[i]: r[i] for i in range(len(columns))} for r in self.db.yield_prefectures()]
#
#        sending_obj = {
#            "length": len(prefs),
#            "body": prefs
#        }
#
#        return json.dumps(sending_obj)
#
#    @_app.route("/api/account", methods=["GET", ])
#    def get_account(self):
#        email = session["username"]
#        user_info = self.db.get_user_account(email)
#        return json.dumps(user_info)
#
#    @_app.route("/api/account", methods=["POST", ])
#    def create_account():
#        got = {key: item for key, item in request.form.items()}
#        return json.dumps(got)
#
#    @_app.route("/api/account", methods=["PUT", ])
#    def update_account():
#        return "Not implemented yet"
#
#
#class DebugView(View):
#    def __init__(self, *args, **kwargs):
#        pass
#
#    @_app.after_request
#    def add_header(r):
#        """
#        Add headers to both force latest IE rendering engine or Chrome Frame,
#        and also to cache the rendered page for 10 minutes.
#        """
#        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#        r.headers["Pragma"] = "no-cache"
#        r.headers["Expires"] = "0"
#        r.headers['Cache-Control'] = 'public, max-age=0'
#        return r
#
#    @_app.route("/api/temp", methods=["GET", ])
#    def get_temp():
#        return json.dumps(request.args)

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

from flask import Flask, session, request, redirect
from necco.config import ServerConfiguration
from necco.views import LoginView, LogoutView, MainView, DebugView
from necco.api import AbilityApi, RequestApi, PrefectureApi, AccountApi
import os


def create_application():
    config = ServerConfiguration()

    app = Flask(
        config.TITLE,
        template_folder=config.DOCROOT,
        static_folder=os.path.join(os.path.dirname(config.DOCROOT), "static"))

    app.secret_key = config.SECRET_KEY
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600

    def before_request():
        """ Function to be called before running app.route().
        """
        if "user_id" in session:
            return None
        if "/login" in request.path:
            return None
        if "/static" in request.path:
            return None

        return redirect("/login")

    app.before_request(before_request)

    return app


def set_url_rules(app):
    app.add_url_rule(rule="/login", view_func=LoginView.as_view("login"))
    app.add_url_rule(rule="/logout", view_func=LogoutView.as_view("logout"))
    app.add_url_rule(rule="/", view_func=MainView.as_view("index"))

    abilities_view = AbilityApi.as_view("abilities")
    app.add_url_rule(rule="/api/abilities", view_func=abilities_view, methods=["GET", ], defaults={"user_id": None})  # get all users' abilities.
    app.add_url_rule(rule="/api/abilities/<int:user_id>", view_func=abilities_view, methods=["GET", "PUT", "POST", "DELETE"])  # get the specified user's ability.

    requests_view = RequestApi.as_view("requests")
    app.add_url_rule(rule="/api/requests", view_func=requests_view, methods=["GET", ], defaults={"user_id": None})  # get all users' requests.
    app.add_url_rule(rule="/api/requests/<int:user_id>", view_func=requests_view, methods=["GET", "PUT", "POST", "DELETE"])  # get the specified user's ability.

    app.add_url_rule(rule="/api/prefs", view_func=PrefectureApi.as_view("prefs"))

    account_view = AccountApi.as_view("account")
    app.add_url_rule(rule="/api/account", view_func=account_view, methods=["POST", ])
    app.add_url_rule(rule="/api/account", view_func=account_view, methods=["GET", "PUT", "DELETE"], defaults={"user_id": None})
    app.add_url_rule(rule="/api/account/<int:user_id>", view_func=account_view, methods=["GET", "PUT", "DELETE"])

    return app


app = set_url_rules(create_application())


def main(app=app):
    def after_request(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    app.after_request(after_request)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    app.debug = True
    app.add_url_rule(rule="/temp", view_func=DebugView.as_view("temp"))

    app.run(host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

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

import argparse
from flask import Flask, session, request, redirect
from necco.config import ServerConfiguration
from necco.views import LoginView, LogoutView, MainView, DebugView
from necco.api import AbilityApi, RequestApi, PrefectureApi, AccountApi
import os
import sys


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="for necco server application")

    parser.add_argument(
        "-c", "--path-config",
        action="store",
        nargs="?",
        default="/etc/necco/necco.ini",
        type=str,
        help="path to necco configuration file")

    return parser.parse_args(args)


def create_application(path_config):
    config = ServerConfiguration(path_config)

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

    def set_url_rules(flask_app):
        flask_app.add_url_rule(rule="/login", view_func=LoginView.as_view("login", config=config))
        flask_app.add_url_rule(rule="/logout", view_func=LogoutView.as_view("logout"))
        flask_app.add_url_rule(rule="/", view_func=MainView.as_view("index", config=config))

        abilities_view = AbilityApi.as_view("abilities", config=config)
        flask_app.add_url_rule(rule="/api/abilities", view_func=abilities_view, methods=["GET", ], defaults={"user_id": None})
        flask_app.add_url_rule(rule="/api/abilities/<int:user_id>", view_func=abilities_view, methods=["GET", "PUT", "POST", "DELETE"])

        requests_view = RequestApi.as_view("requests", config=config)
        flask_app.add_url_rule(rule="/api/requests", view_func=requests_view, methods=["GET", ], defaults={"user_id": None})
        flask_app.add_url_rule(rule="/api/requests/<int:user_id>", view_func=requests_view, methods=["GET", "PUT", "POST", "DELETE"])

        flask_app.add_url_rule(rule="/api/prefs", view_func=PrefectureApi.as_view("prefs"))

        account_view = AccountApi.as_view("account", config=config)
        flask_app.add_url_rule(rule="/api/account", view_func=account_view, methods=["POST", ])
        flask_app.add_url_rule(rule="/api/account", view_func=account_view, methods=["GET", "PUT", "DELETE"], defaults={"user_id": None})
        flask_app.add_url_rule(rule="/api/account/<int:user_id>", view_func=account_view, methods=["GET", "PUT", "DELETE"])

        return flask_app

    return set_url_rules(app)


def create_application_for_debug(path_config):
    flask_app = create_application(path_config)

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

    flask_app.after_request(after_request)
    flask_app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    flask_app.debug = True
    flask_app.add_url_rule(rule="/temp", view_func=DebugView.as_view("temp"))

    return flask_app


def main():
    app = create_application_for_debug(parse_args().path_config)
    app.run(host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

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
from jinja2 import FileSystemLoader
from necco import config
from necco.views import LoginView, LogoutView, MainView


def configure_necco_app():
    app = Flask(config.TITLE)

    app.secret_key = config.SECRET_KEY
    app.jinja_loader = FileSystemLoader([config.DOCROOT, ])
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600

    def prefix():
        """ Function to be called before running app.route().
        """
        if "username" in session:
            return None
        if "/login" in request.path:
            return None
        if "/static" in request.path:
            return None

        return redirect("/login")

    app.before_request(prefix)

    app.add_url_rule(rule="/login", view_func=LoginView.as_view("login"))
    app.add_url_rule(rule="/logout", view_func=LogoutView.as_view("logout"))
    app.add_url_rule(rule="/", view_func=MainView.as_view("index"))

    return app


app = configure_necco_app()


if __name__ == "__main__":
    app.debug = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(host="0.0.0.0", port=5000)

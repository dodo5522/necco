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
from jinja2 import FileSystemLoader
from necco import config
from necco.auth import PasswordAuthentication
from necco.models import NeccoDatabase
from flask import Flask, render_template, session, request, redirect


app = Flask(config.TITLE)
app.secret_key = config.SECRET_KEY
app.jinja_loader = FileSystemLoader(config.DOCROOT)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600
model = NeccoDatabase()


@app.before_request
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


@app.route("/")
def index():
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(
            "login.html",
            title=config.TITLE)

    auth = PasswordAuthentication(
        request.form["email"],
        request.form["password"])

    if not auth.is_authenticated():
        return redirect("/login")

    session["username"] = request.form["email"]
    return redirect("/")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/login")


@app.route("/api/abilities", methods=["GET", ])
def get_abilities():
    columns = ["name", "kana", "detail"]
    abilities = [{columns[i]: r[i] for i in range(len(columns))} for r in model.yield_abilities()]

    sending_obj = {
        "length": len(abilities),
        "body": abilities
    }

    return json.dumps(sending_obj)


@app.route("/api/requests", methods=["GET", ])
def get_requests():
    columns = ["name", "kana", "detail"]
    requests = [{columns[i]: r[i] for i in range(len(columns))} for r in model.yield_requests()]

    sending_obj = {
        "length": len(requests),
        "body": requests
    }

    return json.dumps(sending_obj)


@app.route("/api/prefs", methods=["GET", ])
def get_prefectures():
    columns = ["id", "name"]
    prefs = [{columns[i]: r[i] for i in range(len(columns))} for r in model.yield_prefectures()]

    sending_obj = {
        "length": len(prefs),
        "body": prefs
    }

    return json.dumps(sending_obj)


@app.route("/api/account", methods=["GET", ])
def get_account():
    email = session["username"]
    user_info = model.get_user_account(email)
    return json.dumps(user_info)


@app.route("/api/account", methods=["POST", ])
def create_account():
    return "Not implemented yet"


@app.route("/api/account", methods=["PUT", ])
def update_account():
    return "Not implemented yet"

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
from necco.models import NeccoDbWrapper
from flask import Flask, render_template, session, request, redirect
import random
import string


app = Flask(config.TITLE)
app.secret_key = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(128)])
model = NeccoDbWrapper()


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


@app.route("/api/ability-list", methods=["GET", ])
def get_ability_list():
    columns = ["name", "kana", "detail"]
    abilities = [{columns[i]: r[i] for i in range(3)} for r in model.get_abilities()]

    return json.dumps(abilities)


@app.route("/api/request-list", methods=["GET", ])
def get_request_list():
    columns = ["name", "kana", "detail"]
    requests = [{columns[i]: r[i] for i in range(3)} for r in model.get_requests()]

    return json.dumps(requests)

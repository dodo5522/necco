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

import os
import sqlite3
from werkzeug.security import generate_password_hash

# Keep the below queries same as written on data/scheme.sql.

_QUERY_CREATE_TABLE_USER = """
CREATE TABLE IF NOT EXISTS User (
    id_         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    createdAt   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email       VARCHAR(321) DEFAULT '' NOT NULL,
    password_   VARCHAR(128) NOT NULL,
    isAdmin     BOOLEAN DEFAULT 0 NOT NULL
);"""

_QUERY_CREATE_TABLE_HISTORY = """
CREATE TABLE IF NOT EXISTS History (
    id_           INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    createdAt     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    payerUserId   INTEGER NOT NULL,
    providedAt    DATETIME NOT NULL,
    payeeUserId   INTEGER NOT NULL,
    what          VARCHAR(1024) NOT NULL,
    priceNecco    INTEGER DEFAULT 0 NOT NULL,
    priceYen      INTEGER DEFAULT 0 NOT NULL
);"""

_QUERY_CREATE_TABLE_PROFILE = """
CREATE TABLE IF NOT EXISTS Profile (
    id_           INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    createdAt     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    userId        INTEGER NOT NULL,
    lastName      VARCHAR(128)    NOT NULL,
    firstName     VARCHAR(128)    NOT NULL,
    lastKanaName  VARCHAR(128)    NOT NULL,
    firstKanaName VARCHAR(128)    NOT NULL,
    nickName      VARCHAR(128)    DEFAULT '' NOT NULL,
    phoneNumber   VARCHAR(32)     DEFAULT '' NOT NULL,
    faxNumber     VARCHAR(32)     DEFAULT '' NOT NULL,
    prefectureId INTEGER DEFAULT 1  NOT NULL,
    address       VARCHAR(16)  DEFAULT '' NOT NULL,
    streetAddress VARCHAR(128) DEFAULT '' NOT NULL,
    latitude      DOUBLE(7,5) DEFAULT 0.0 NOT NULL,
    longitude     DOUBLE(8,5) DEFAULT 0.0 NOT NULL,
    profile       VARCHAR(4096)   DEFAULT '' NOT NULL
);"""

_QUERY_CREATE_TABLE_PREFECTURE = """
CREATE TABLE IF NOT EXISTS Prefecture (
    id_        INTEGER PRIMARY KEY AUTOINCREMENT,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name_ VARCHAR(16) UNIQUE NOT NULL
);"""

_QUERY_CREATE_TABLE_USERS_ABILITY = """
CREATE TABLE IF NOT EXISTS UsersAbility (
    id_        INTEGER PRIMARY KEY AUTOINCREMENT,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    userId     INTEGER NOT NULL,
    abilityId  INTEGER NOT NULL
);"""

_QUERY_CREATE_TABLE_ABILITY = """
CREATE TABLE IF NOT EXISTS Ability (
    id_        INTEGER PRIMARY KEY AUTOINCREMENT,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    genre      VARCHAR(1024) DEFAULT '' NOT NULL,
    detail     VARCHAR(1024) DEFAULT '' NOT NULL
);"""

_QUERY_CREATE_TABLE_USERS_REQUEST = """
CREATE TABLE IF NOT EXISTS UsersRequest (
    id_        INTEGER PRIMARY KEY AUTOINCREMENT,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    userId     INTEGER NOT NULL,
    requestId  INTEGER NOT NULL
);"""

_QUERY_CREATE_TABLE_REQUEST = """
CREATE TABLE IF NOT EXISTS Request (
    id_        INTEGER PRIMARY KEY AUTOINCREMENT,
    createdAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updatedAt  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    genre      VARCHAR(1024) DEFAULT '' NOT NULL,
    detail     VARCHAR(1024) DEFAULT '' NOT NULL
);"""

_QUERIES_CREATE_TABLE = [
    _QUERY_CREATE_TABLE_ABILITY,
    _QUERY_CREATE_TABLE_HISTORY,
    _QUERY_CREATE_TABLE_PREFECTURE,
    _QUERY_CREATE_TABLE_PROFILE,
    _QUERY_CREATE_TABLE_REQUEST,
    _QUERY_CREATE_TABLE_USER,
    _QUERY_CREATE_TABLE_USERS_ABILITY,
    _QUERY_CREATE_TABLE_USERS_REQUEST,
]

_QUERY_INSERT = "INSERT INTO {TABLE}({COLUMNS}) VALUES ({VALUES});"

_QUERIES_INSERT = [
    _QUERY_INSERT.format(TABLE="Ability", COLUMNS="id_, genre, detail", VALUES="1, '', '植物の水やり'"),
    _QUERY_INSERT.format(TABLE="Ability", COLUMNS="id_, genre, detail", VALUES="2, '', '子守り'"),
    _QUERY_INSERT.format(TABLE="Ability", COLUMNS="id_, genre, detail", VALUES="3, '', '犬の散歩'"),
    _QUERY_INSERT.format(TABLE="Prefecture", COLUMNS="id_, name_", VALUES="11, '埼玉県'"),
    _QUERY_INSERT.format(TABLE="Prefecture", COLUMNS="id_, name_", VALUES="12, '千葉県'"),
    _QUERY_INSERT.format(TABLE="Prefecture", COLUMNS="id_, name_", VALUES="13, '東京都'"),
    _QUERY_INSERT.format(
        TABLE="Profile",
        COLUMNS="id_, userId, lastName, firstName, lastKanaName, firstKanaName, nickName, phoneNumber, faxNumber, prefectureId, address, streetAddress, latitude, longitude, profile",
        VALUES="0, 1, '山田', '太郎', 'やまだ', 'たろう', 'たろ', '010-010-010', '101-101-101', 13, '昭島市', '玉川町', '0.0001', '0.0002', 'あけおめ'"),
    _QUERY_INSERT.format(
        TABLE="Profile",
        COLUMNS="id_, userId, lastName, firstName, lastKanaName, firstKanaName, nickName, phoneNumber, faxNumber, prefectureId, address, streetAddress, latitude, longitude, profile",
        VALUES="1, 2, '山田', '次郎', 'やまだ', 'じろう', 'じろ', '020-020-020', '202-202-202', 13, '昭島市', '田中町', '0.0003', '0.0004', 'ことよろ'"),
    _QUERY_INSERT.format(TABLE="Request", COLUMNS="id_, genre, detail", VALUES="1, '', '子守り'"),
    _QUERY_INSERT.format(TABLE="Request", COLUMNS="id_, genre, detail", VALUES="2, '', '家に車が無い為、何かの機会に同乗させて頂けると嬉しい'"),
    _QUERY_INSERT.format(TABLE="Request", COLUMNS="id_, genre, detail", VALUES="3, '', '妊娠出産で大変な時の、元気いっぱいの上の子2人のお世話'"),
    _QUERY_INSERT.format(TABLE="User", COLUMNS="id_, email, password_, isAdmin", VALUES="1, 'taro.yamada@temp.com', '{}', 0".format(generate_password_hash("taro's password"))),
    _QUERY_INSERT.format(TABLE="User", COLUMNS="id_, email, password_, isAdmin", VALUES="2, 'jiro.yamada@temp.com', '{}', 1".format(generate_password_hash("jiro's password"))),
    _QUERY_INSERT.format(TABLE="UsersAbility", COLUMNS="id_, userId, abilityId", VALUES="0, 1, 1"),
    _QUERY_INSERT.format(TABLE="UsersAbility", COLUMNS="id_, userId, abilityId", VALUES="1, 1, 2"),
    _QUERY_INSERT.format(TABLE="UsersAbility", COLUMNS="id_, userId, abilityId", VALUES="2, 1, 3"),
    _QUERY_INSERT.format(TABLE="UsersAbility", COLUMNS="id_, userId, abilityId", VALUES="3, 2, 2"),
    _QUERY_INSERT.format(TABLE="UsersRequest", COLUMNS="id_, userId, requestId", VALUES="0, 1, 1"),
    _QUERY_INSERT.format(TABLE="UsersRequest", COLUMNS="id_, userId, requestId", VALUES="1, 1, 3"),
    _QUERY_INSERT.format(TABLE="UsersRequest", COLUMNS="id_, userId, requestId", VALUES="2, 2, 1"),
    _QUERY_INSERT.format(TABLE="UsersRequest", COLUMNS="id_, userId, requestId", VALUES="3, 2, 2"),
    _QUERY_INSERT.format(TABLE="UsersRequest", COLUMNS="id_, userId, requestId", VALUES="4, 2, 3"),
]


class AbstractAccessorToTestData(object):
    _DB_PATH = "/tmp/necco_{}_test.db"

    def get_db_path(self):
        """ Implement like below.

        def get_db_path(self):
            return self._DB_PATH.format(self.__class__.__name__)
        """
        raise NotImplementedError

    def remove_db_if_exists(self):
        if os.path.exists(self.get_db_path()):
            os.remove(self.get_db_path())

    def initialize_db(self):
        """ Create database, table, and data for test.
            If already exists, remove it at once.

        raises:
            OperationalError: Permission denied, etc.
        """
        self.remove_db_if_exists()

        with sqlite3.connect(self.get_db_path()) as con:
            for query in _QUERIES_CREATE_TABLE:
                con.execute(query)

            for query in _QUERIES_INSERT:
                con.execute(query)

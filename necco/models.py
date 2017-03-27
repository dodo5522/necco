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

from necco import config
import sqlalchemy


class MySqlDriver(object):
    """ Temprary implementation of DB driver API class.

    Args:
        user: User name with read priviledged.
        password: The user's Password to access DB.
        server: DB host address.
        port: DB host port.
        database: DB name to access.
    """

    def __init__(self, user, password, server, port, database):
        self.engine = sqlalchemy.create_engine(
            "mysql+pymysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}?charset=utf8".format(
                USER=user, PASSWORD=password, SERVER=server, PORT=port, DB=database))

    def execute(self, query):
        """ Run the specified query string and get all data.

        Args:
            query: query string like "SELECT * from some_table;".

        Returns:
            Got result like some array or table.
        """
        return self.engine.execute(query).fetchall()


_db = MySqlDriver(
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    server=config.MYSQL_SERVER,
    port=config.MYSQL_PORT,
    database=config.MYSQL_DB)


class NeccoDbWrapper(object):
    _QUERY_GET_REQUESTS = """
        SELECT Profile.name_, Profile.kana, Request.detail FROM User
            INNER JOIN Profile ON User.id = Profile.user_id
            INNER JOIN UsersRequest ON User.id = UsersRequest.user_id
            INNER JOIN Request ON UsersRequest.request_id = Request.id;"""

    _QUERY_GET_ABILITIES = """
        SELECT Profile.name_, Profile.kana, Ability.detail FROM Profile
            INNER JOIN User ON Profile.user_id = User.id
            INNER JOIN UsersAbility ON User.id = UsersAbility.user_id
            INNER JOIN Ability ON UsersAbility.ability_id = Ability.id;"""

    def __init__(self, db_=_db):
        self._db = db_

    def get_requests(self):
        return self._db.execute(self._QUERY_GET_REQUESTS)

    def get_abilities(self):
        return self._db.execute(self._QUERY_GET_ABILITIES)

    def get_hashed_password(self, id_):
        record = self._db.execute("SELECT password_ FROM User WHERE email = '{}'".format(id_))

        if not record:
            return None

        return record[0][0]

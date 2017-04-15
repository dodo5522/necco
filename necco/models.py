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
from sqlalchemy import create_engine, MetaData


class NeccoDatabase(object):
    __instance = None

    def __new__(
            cls,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            server=config.MYSQL_SERVER,
            port=config.MYSQL_PORT,
            db=config.MYSQL_DB):

        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

            engine = create_engine(
                "mysql+pymysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}?charset=utf8".format(
                    USER=user,
                    PASSWORD=password,
                    SERVER=server,
                    PORT=port,
                    DB=db))

            cls.__db_meta = MetaData(bind=engine)
            cls.__db_meta.reflect()

            for name, table in cls.__db_meta.tables.items():
                setattr(cls, name, table)

        return cls.__instance

    def __init__(self, *args, **kwargs):
        pass

    def yield_requests(self):
        """ Generator function which returns request records with below query.

            SELECT Profile.name_, Profile.kana, Request.detail FROM User
                INNER JOIN Profile ON User.id = Profile.user_id
                INNER JOIN UsersRequest ON User.id_ = UsersRequest.user_id
                INNER JOIN Request ON UsersRequest.request_id = Request.id_;
        """
        columns = [self.Profile.c.name_, self.Profile.c.kana, self.Request.c.detail]

        joined_query = self.User.join(self.Profile, self.User.c.id_ == self.Profile.c.user_id)
        joined_query = joined_query.join(self.UsersRequest, self.User.c.id_ == self.UsersRequest.c.user_id)
        joined_query = joined_query.join(self.Request, self.UsersRequest.c.request_id == self.Request.c.id_)
        joined_query = joined_query.select(self.User.c.id_)

        for record in joined_query.with_only_columns(columns).execute():
            yield record

    def yield_abilities(self):
        """ Generator function which returns ability records with below query.

            SELECT Profile.name_, Profile.kana, Ability.detail FROM User
                INNER JOIN Profile ON Profile.user_id = User.id_
                INNER JOIN UsersAbility ON User.id_ = UsersAbility.user_id
                INNER JOIN Ability ON UsersAbility.ability_id = Ability.id_;
        """
        columns = [self.Profile.c.name_, self.Profile.c.kana, self.Ability.c.detail]

        joined_query = self.User.join(self.Profile, self.User.c.id_ == self.Profile.c.user_id)
        joined_query = joined_query.join(self.UsersAbility, self.User.c.id_ == self.UsersAbility.c.user_id)
        joined_query = joined_query.join(self.Ability, self.UsersAbility.c.ability_id == self.Ability.c.id_)
        joined_query = joined_query.select(self.User.c.id_)

        for record in joined_query.with_only_columns(columns).execute():
            yield record

    def get_hashed_password(self, email):
        proxy = self.User.select(self.User.c.email == email).execute()

        if not proxy.rowcount:
            raise ValueError("Account not found.")

        index = proxy.keys().index("password_")
        password = proxy.fetchone()[index]

        return password

    def yield_prefectures(self):
        """ Generator function which returns prefectures with below query.

            SELECT Prefecture.id_, Prefecture.name_ FROM Prefecture;
        """
        columns = [self.Prefecture.c.id_, self.Prefecture.c.name_]

        query = self.Prefecture.select().with_only_columns(columns)

        for record in query.execute():
            yield record

    def get_user_account(self, email):
        """ Getter function returns the specified user infomation.

            SELECT Profile.name_, Profile.kana, Profile.nickname, User.email, User.password_,
                   Prefecture.name_, Profile.city, Profile.latitude, Profile.longitude, Profile.phone, Profile.fax
                   from Profile inner join User on Profile.user_id = User.id_ inner join Prefecture on Profile.prefecture_id = Prefecture.id_;
        """
        columns = [
            self.Profile.c.name_, self.Profile.c.kana, self.Profile.c.nickname,
            self.User.c.email, self.User.c.password_, self.Prefecture.c.name_,
            self.Profile.c.city, self.Profile.c.latitude, self.Profile.c.longitude,
            self.Profile.c.phone, self.Profile.c.fax]

        joined_query = self.User.join(self.Profile, self.User.c.id_ == self.Profile.c.user_id)
        joined_query = joined_query.join(self.Prefecture, self.Profile.c.prefecture_id == self.Prefecture.c.id_)
        joined_query = joined_query.select(self.User.c.email == email).with_only_columns(columns)

        record = joined_query.execute().fetchone()

        return {str(key): str(value) for key, value in zip(columns, record)}

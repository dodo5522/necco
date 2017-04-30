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
from sqlalchemy.sql import func


class DbBase(object):
    __instance = None

    def __new__(
            cls,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            server=config.MYSQL_SERVER,
            port=config.MYSQL_PORT,
            db=config.MYSQL_DB,
            url=None):

        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

            engine = create_engine(
                "mysql+pymysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}?charset=utf8".format(
                    USER=user,
                    PASSWORD=password,
                    SERVER=server,
                    PORT=port,
                    DB=db)) if url is None else create_engine(url)

            cls.__db_meta = MetaData(bind=engine)
            cls.__db_meta.reflect()

            for name, table in cls.__db_meta.tables.items():
                setattr(cls, name, table)

        return cls.__instance


class BaseModel(object):
    def __init__(self, db=None):
        self._db = db if db else DbBase()

    def get_columns(self):
        raise NotImplementedError

    def yield_record(self):
        raise NotImplementedError


class AccountModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.account_columns = [
            # db, html
            (self._db.Profile.c.lastName, "lastName"),
            (self._db.Profile.c.firstName, "firstName"),
            (self._db.Profile.c.lastKanaName, "lastKanaName"),
            (self._db.Profile.c.firstKanaName, "firstKanaName"),
            (self._db.Profile.c.nickName, "nickName"),
            (self._db.User.c.email, "email"),
            (self._db.Prefecture.c.name_, "prefecture"),
            (self._db.Profile.c.address, "address"),
            (self._db.Profile.c.streetAddress, "streetAddress"),
            (self._db.Profile.c.phoneNumber, "phoneNumber"),
            (self._db.Profile.c.faxNumber, "faxNumber"),
            (self._db.Profile.c.profile, "profile"),
        ]

    def get_columns(self):
        return [c[1] for c in self.account_columns]

    def yield_record(self):
        yield None

    def get_hashed_password(self, email):
        proxy = self._db.User.select(self._db.User.c.email == email).execute()

        if not proxy.rowcount:
            raise ValueError("Account not found.")

        index = proxy.keys().index("password_")
        password = proxy.fetchone()[index]

        return password

    def get_user_account(self, email):
        """ Getter function returns the specified user infomation.

            SELECT Profile.name_, Profile.kana, Profile.nickname, ... from Profile
                   inner join User on Profile.userId = User.id_
                   inner join Prefecture on Profile.prefectureId = Prefecture.id_;
        """

        joined_query = self._db.User.join(
            self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        joined_query = joined_query.join(
            self._db.Prefecture, self._db.Profile.c.prefectureId == self._db.Prefecture.c.id_)
        joined_query = joined_query.select(
            self._db.User.c.email == email).with_only_columns([c[0] for c in self.account_columns])

        record = joined_query.execute().fetchone()

        return {str(key): str(value) for key, value in zip((c[1] for c in self.account_columns), record)}


class AbilityModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ability_columns = [
            (self._db.Profile.c.lastName, "lastName"),
            (self._db.Profile.c.firstName, "firstName"),
            (self._db.Profile.c.lastKanaName, "lastKanaName"),
            (self._db.Profile.c.firstKanaName, "firstKanaName"),
            (self._db.Ability.c.detail, "detail"),
        ]

    def get_columns(self):
        return [c[1] for c in self.ability_columns]

    def yield_record(self):
        """ Generator function which returns ability records with below query.

            SELECT Profile.lastName, Profile.firstName, ... FROM User
                INNER JOIN Profile ON Profile.userId = User.id_
                INNER JOIN UsersAbility ON User.id_ = UsersAbility.userId
                INNER JOIN Ability ON UsersAbility.abilityId = Ability.id_;
        """

        joined_query = self._db.User.join(self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        joined_query = joined_query.join(self._db.UsersAbility, self._db.User.c.id_ == self._db.UsersAbility.c.userId)
        joined_query = joined_query.join(self._db.Ability, self._db.UsersAbility.c.abilityId == self._db.Ability.c.id_)
        joined_query = joined_query.select()
        joined_query = joined_query.with_only_columns([c[0] for c in self.ability_columns]).execute()

        while True:
            record = joined_query.fetchone()
            if not record:
                break
            yield record


class RequestModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.request_columns = [
            (self._db.Profile.c.lastName, "lastName"),
            (self._db.Profile.c.firstName, "firstName"),
            (self._db.Profile.c.lastKanaName, "lastKanaName"),
            (self._db.Profile.c.firstKanaName, "firstKanaName"),
            (self._db.Request.c.detail, "detail"),
        ]

    def _get_request_count(self):
        """ Get the number of requests.

            SELECT COUNT(*) FROM Request
                INNER JOIN UsersRequest ON UsersRequest.requestId = Request.id_;
        """

        joined_query = self._db.Request.join(
            self._db.UsersRequest, self._db.UsersRequest.c.requestId == self._db.Request.c.id_)
        joined_query = joined_query.select().with_only_columns([func.count()])
        res = joined_query.execute()
        return [_ for _ in res][0][0]

    def get_columns(self):
        return [c[1] for c in self.request_columns]

    def yield_record(self):
        """ Generator function which returns request records with below query.

            SELECT Profile.lastName, Profile.firstName, Profile.lastKanaName, Profile.firstKanaName, Request.detail FROM User
                INNER JOIN Profile ON User.id = Profile.userId
                INNER JOIN UsersRequest ON User.id_ = UsersRequest.userId
                INNER JOIN Request ON UsersRequest.requestId = Request.id_;
        """

        joined_query = self._db.User.join(
            self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        joined_query = joined_query.join(
            self._db.UsersRequest, self._db.User.c.id_ == self._db.UsersRequest.c.userId)
        joined_query = joined_query.join(
            self._db.Request, self._db.UsersRequest.c.requestId == self._db.Request.c.id_)
        joined_query = joined_query.select()
        joined_query = joined_query.with_only_columns([c[0] for c in self.request_columns]).execute()

        while True:
            record = joined_query.fetchone()
            if not record:
                break
            yield record


class PrefectureModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get_columns(self):
        return [
            self._db.Prefecture.c.id_,
            self._db.Prefecture.c.name_
        ]

    def yield_record(self):
        """ Generator function which returns prefectures with below query.

            SELECT Prefecture.id_, Prefecture.name_ FROM Prefecture;
        """
        query = self._db.Prefecture.select().with_only_columns(self.get_columns())

        for record in query.execute():
            yield record

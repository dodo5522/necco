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

from collections import OrderedDict
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash


class INeccoDb(object):
    """ Interface to necco database.
    """
    pass


class SqliteDb(INeccoDb):
    """ To create instance of Sqlite DB. This class to use mainly for testing.

    arguments:
        path_to_db: Path to your Sqlite DB file.
    """
    def __init__(self, path_to_db, **kwargs):
        self.__db_meta = MetaData(
            bind=create_engine("sqlite:///" + path_to_db))
        self.__db_meta.reflect()

        for name, table in self.__db_meta.tables.items():
            setattr(self, name, table)


class MySqlDb(INeccoDb):
    """ To create an instance of MySQL DB as singleton.

    arguments:
        user: User name to login MySQL DB.
        pasword: Password for the above user.
        server: IP address or something of MySQL server.
        port: Port number.
        db_name: DB name.
    """
    __instance = None

    def __new__(cls, user, password, server, port, db_name):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

            engine = create_engine(
                "mysql+pymysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}?charset=utf8".format(
                    USER=user,
                    PASSWORD=password,
                    SERVER=server,
                    PORT=port,
                    DB=db_name),
                pool_recycle=14400)

            cls.__db_meta = MetaData(bind=engine)
            cls.__db_meta.reflect()

            for name, table in cls.__db_meta.tables.items():
                setattr(cls, name, table)

        return cls.__instance


class AbstractModel(object):
    """ Abstract base model to provide APIs to access database for necco.

    arguments:
        config: Configuration object of necco.config.Configuration.

    keyword arguments:
        db: Dabase instance with INeccoDb. This's mainly used for testing.
    """

    def __init__(self, config, db=None, **kwargs):
        self._db = db if db else MySqlDb(
            config.SQL_USER,
            config.SQL_PASSWORD,
            config.SQL_SERVER,
            config.SQL_PORT,
            config.SQL_DB)

    def get_all_column(self):
        raise NotImplementedError

    def yield_record(self, columns=None):
        raise NotImplementedError


class AccountModel(AbstractModel):
    """ Model to provide APIs to access user's account on necco DB.

    arguments:
        config: Configuration object of necco.config.Configuration.

    keyword arguments:
        db: Dabase instance with INeccoDb. This's mainly used for testing.
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, db=kwargs.get("db"))
        self.account_columns = OrderedDict()
        self.account_columns["lastName"] = self._db.Profile.c.lastName
        self.account_columns["firstName"] = self._db.Profile.c.firstName
        self.account_columns["lastKanaName"] = self._db.Profile.c.lastKanaName
        self.account_columns["firstKanaName"] = self._db.Profile.c.firstKanaName
        self.account_columns["nickName"] = self._db.Profile.c.nickName
        self.account_columns["email"] = self._db.User.c.email
        self.account_columns["prefecture"] = self._db.Prefecture.c.name_
        self.account_columns["address"] = self._db.Profile.c.address
        self.account_columns["streetAddress"] = self._db.Profile.c.streetAddress
        self.account_columns["phoneNumber"] = self._db.Profile.c.phoneNumber
        self.account_columns["faxNumber"] = self._db.Profile.c.faxNumber
        self.account_columns["profile"] = self._db.Profile.c.profile

    def get_all_column(self):
        return self.account_columns.keys()

    def get_hashed_password(self, user_id):
        proxy = self._db.User.select(self._db.User.c.id_ == user_id).execute()

        if not proxy.rowcount:
            raise ValueError("Account not found.")

        index = proxy.keys().index("password_")
        password = proxy.fetchone()[index]

        return password

    def get_id(self, email):
        """ Getter function returns user id against the specified email.
        """

        query = self._db.User.select(self._db.User.c.email == email)
        query = query.with_only_columns([self._db.User.c.id_, ])
        record = query.execute().fetchone()

        return record[0] if record else 0

    def get_email(self, user_id):
        """ Getter function returns the specified user's email.
        """

        query = self._db.User.select(self._db.User.c.id_ == user_id)
        query = query.with_only_columns([self._db.User.c.email, ])

        record = query.execute().fetchone()
        return record[0]

    def get_all(self, user_id):
        """ Getter function returns the specified user infomation.

            SELECT Profile.name_, Profile.kana, Profile.nickname, ... from Profile
                   inner join User on Profile.userId = User.id_
                   inner join Prefecture on Profile.prefectureId = Prefecture.id_;
        """

        query = self._db.User.join(
            self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        query = query.join(
            self._db.Prefecture, self._db.Profile.c.prefectureId == self._db.Prefecture.c.id_)
        query = query.select(
            self._db.User.c.id_ == user_id).with_only_columns(self.account_columns.values())

        record = query.execute().fetchone()

        return {str(key): str(value) for key, value in zip(self.account_columns.keys(), record)}

    def is_admin(self, user_id):
        """ Get isAdmin flag's value. """

        query = self._db.User.select(self._db.User.c.id_ == user_id)
        query = query.with_only_columns([self._db.User.c.isAdmin, ])

        record = query.execute().fetchone()

        return bool(record[0]) if record is not None else False

    def update_user_with(self, id_, password_, email):
        hashed_password = generate_password_hash(password_)

        query = self._db.User.update()
        query = query.where(self._db.User.c.id_ == id_)
        query = query.values(email=email)
        query = query.values(password_=hashed_password)
        query = query.values(updatedAt=datetime.now())

        query.execute()

    def update_profile_with(self, id_, **kwargs):
        params = {"updatedAt": datetime.now()}
        for column in self._db.Profile.c.keys():
            val = kwargs.get(column)
            if val:
                params[column] = val

        query = self._db.Profile.update()
        query = query.where(self._db.Profile.c.userId == id_)
        query = query.values(**params)

        query.execute()

    def update_account_with(self, id_, **kwargs):
        """ Update account information against the specified user id.
        """
        self.update_user_with(id_, kwargs["password_"], kwargs["email"])
        self.update_profile_with(id_, **kwargs)
        # TODO:
        # self.update_prefecture_with(id_, kwargs)

    def create_account_with(self, **kwargs):
        """ Create new account information. user id is generated automatically.

        Args:
            email, password_, ...: Parameters needed for user to be created.

        Returns:
            user id if success, else 0.
        """
        def create_user(params):
            hashed_password = generate_password_hash(params["password_"])

            query = self._db.User.insert()
            query = query.values(email=params["email"])
            query = query.values(password_=hashed_password)
            query = query.values(isAdmin=params["isAdmin"])
            query.execute()

            return self.get_id(email)

        def create_profile(user_id, params):
            query = self._db.Profile.insert()
            query = query.values(userId=user_id)
            query = query.values(**params)
            query.execute()

        email = kwargs.get("email")

        # error if user already exists
        if self.get_id(email):
            return 0

        params = {}
        for column in self._db.Profile.c.keys():
            val = kwargs.get(column)
            if val:
                params[column] = val

        user_id = create_user(kwargs)
        create_profile(user_id, params)

        return self.get_id(email)


class AbilityModel(AbstractModel):
    """ Model to provide APIs to access user's ability on necco DB.

    arguments:
        config: Configuration object of necco.config.Configuration.

    keyword arguments:
        db: Dabase instance with INeccoDb. This's mainly used for testing.
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, db=kwargs.get("db"))
        self.ability_columns = {
            "lastName": self._db.Profile.c.lastName,
            "firstName": self._db.Profile.c.firstName,
            "lastKanaName": self._db.Profile.c.lastKanaName,
            "firstKanaName": self._db.Profile.c.firstKanaName,
            "genre": self._db.Ability.c.genre,
            "detail": self._db.Ability.c.detail,
        }

    def get_all_column(self):
        return [k for k in self.ability_columns.keys()]

    def yield_record(self, user_ids=[], columns=None):
        """ Generator function which returns ability records with the specified users and below query.

            SELECT Profile.lastName, Profile.firstName, ... FROM User
                INNER JOIN Profile ON Profile.userId = User.id_
                INNER JOIN UsersAbility ON User.id_ = UsersAbility.userId
                INNER JOIN Ability ON UsersAbility.abilityId = Ability.id_;
        """
        filter_ = None
        if user_ids:
            filter_ = self._db.User.c.id_ == user_ids[0]
            for user_id in user_ids[1:]:
                filter_ |= self._db.User.c.id_ == user_id

        if columns:
            columns = [col for col in columns if col in self.ability_columns.keys()]
        else:
            columns = [col for col in self.ability_columns.keys()]
        db_columns = [self.ability_columns.get(col) for col in columns]

        joined_query = self._db.User.join(self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        joined_query = joined_query.join(self._db.UsersAbility, self._db.User.c.id_ == self._db.UsersAbility.c.userId)
        joined_query = joined_query.join(self._db.Ability, self._db.UsersAbility.c.abilityId == self._db.Ability.c.id_)
        selected_query = joined_query.select()

        # if filter_:  # not operated... why?
        if filter_ is not None:
            selected_query = selected_query.where(filter_)

        executed = selected_query.with_only_columns(db_columns).execute()

        for record in executed.fetchall():
            yield {columns[i]: r for i, r in enumerate(record)}


class RequestModel(AbstractModel):
    """ Model to provide APIs to access user's requests on necco DB.

    arguments:
        config: Configuration object of necco.config.Configuration.

    keyword arguments:
        db: Dabase instance with INeccoDb. This's mainly used for testing.
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, db=kwargs.get("db"))
        self.request_columns = {
            "lastName": self._db.Profile.c.lastName,
            "firstName": self._db.Profile.c.firstName,
            "lastKanaName": self._db.Profile.c.lastKanaName,
            "firstKanaName": self._db.Profile.c.firstKanaName,
            "genre": self._db.Request.c.genre,
            "detail": self._db.Request.c.detail,
        }

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

    def get_all_column(self):
        return [k for k in self.request_columns.keys()]

    def yield_record(self, user_ids=[], columns=None):
        """ Generator function which returns request records with below query.

            SELECT Profile.lastName, Profile.firstName, Profile.lastKanaName, Profile.firstKanaName, Request.detail FROM User
                INNER JOIN Profile ON User.id = Profile.userId
                INNER JOIN UsersRequest ON User.id_ = UsersRequest.userId
                INNER JOIN Request ON UsersRequest.requestId = Request.id_;
        """
        filter_ = None
        if user_ids:
            filter_ = self._db.User.c.id_ == user_ids[0]
            for user_id in user_ids[1:]:
                filter_ |= self._db.User.c.id_ == user_id

        if columns:
            columns = [col for col in columns if col in self.request_columns.keys()]
        else:
            columns = [col for col in self.request_columns.keys()]
        db_columns = [self.request_columns.get(col) for col in columns]

        joined_query = self._db.User.join(self._db.Profile, self._db.User.c.id_ == self._db.Profile.c.userId)
        joined_query = joined_query.join(self._db.UsersRequest, self._db.User.c.id_ == self._db.UsersRequest.c.userId)
        joined_query = joined_query.join(self._db.Request, self._db.UsersRequest.c.requestId == self._db.Request.c.id_)
        selected_query = joined_query.select()

        if filter_ is not None:
            selected_query = selected_query.where(filter_)

        executed = selected_query.with_only_columns(db_columns).execute()

        for record in executed.fetchall():
            yield {columns[i]: r for i, r in enumerate(record)}


class PrefectureModel(AbstractModel):
    def __init__(self, config, **kwargs):
        super().__init__(config, db=kwargs.get("db"))

    def get_all_column(self):
        return [
            self._db.Prefecture.c.id_,
            self._db.Prefecture.c.name_
        ]

    def yield_record(self, columns=None):
        """ Generator function which returns prefectures with below query.

            SELECT Prefecture.id_, Prefecture.name_ FROM Prefecture;
        """
        query = self._db.Prefecture.select().with_only_columns(self.get_all_column())

        for record in query.execute():
            yield record

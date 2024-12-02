# BSD 3-Clause License
# Copyright (c) 2024, mac
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

import os
import logging
import sqlalchemy as db
from datetime import datetime


class CrypterDb(object):
    def __init__(self, dbName, dbPath):
        self.dbName = dbName
        self.dbFile = f"{os.path.join(dbPath, dbName)}.db"
        self.engine = db.create_engine(f"sqlite:///{self.dbFile}")
        self.connection = None
        self.meta = db.MetaData()

    def __enter__(self):
        self.connection = self.engine.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.connection.close()
        self.connection = None

    def setup(self):
        secret = db.Table("secret", self.meta,
                          db.Column("Id", db.Integer(), nullable=False, primary_key=True, autoincrement=True),
                          db.Column("tool_seed", db.String(255), nullable=False),
                          db.Column("user_seed", db.String(255), nullable=False),
                          db.Column("created_at", db.DATETIME, nullable=True, default=datetime.now()),
                          db.Column("modified_at", db.DATETIME, nullable=True, default=datetime.now()),
                          db.Column("is_deleted", db.Boolean, nullable=True, default=False),
                          sqlite_autoincrement=True
        )
        records = db.Table("records", self.meta,
                    db.Column("Id", db.Integer(), nullable=False, primary_key=True, autoincrement=True),
                    db.Column("key_name", db.String(255), nullable=False),
                    db.Column("user_name", db.String(255), nullable=False),
                    db.Column("user_password", db.String(255), nullable=False),
                    db.Column("created_at", db.DATETIME, nullable=True, default=datetime.now()),
                    db.Column("modified_at", db.DATETIME, nullable=True, default=datetime.now()),
                    db.Column("is_deleted", db.Boolean, nullable=True, default=False),
                    sqlite_autoincrement=True
        )
        self.meta.create_all(self.engine)

    def cleanup(self):
        pass

    def execute(self, query):
        result = self.connection.execute(query)
        return result

    def insert(self, tableName, values):
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        query = table.insert().values(**values).returning(table.c.key_name, table.c.user_name, table.c.user_password)
        result = self.execute(query).fetchall()
        return result

    def update(self):
        pass

    def get(self, tableName, keyNames):
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        query = table.select().with_only_columns(table.columns.key_name, table.columns.user_name, table.columns.user_password)
        if keyNames:
            query = query.where(table.columns.key_name.in_(keyNames))
        return self.execute(query).fetchall()

    def delete(self, tableName, keyNames):
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        result = list()
        if not keyNames:
            table.drop(self.engine)
            return result
        query = table.delete().where(table.columns.key_name.in_(keyNames)).returning(table.c.key_name, table.c.user_name, table.c.user_password)
        result = self.execute(query).fetchall()
        return result
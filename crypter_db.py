import os
import logging
import sqlalchemy as db
from datetime import datetime


class CrypterDb(object):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__call__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, dbName, dbPath):
        self.dbName = dbName
        self.dbFile = f"{os.path.join(dbPath, dbName)}.db"
        self.engine = db.create_engine(f"sqlite:///{self.dbFile}")
        self.connection = None
        self.meta = db.MetaData()

    def connect(self):
        self.connection = self.engine.connect()

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

    def insert(self, tableName, values):
        print(tableName, values)
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        query = table.insert().values(**values)
        return self.execute(query)

    def update(self):
        pass

    def get(self, keyName, tableName):
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        query = table.select()
        return self.execute(query).fetchall()

    def delete(self):
        table = db.Table(tableName, self.meta, autoload_with=self.engine)
        table.drop(self.engine)

    def execute(self, query):
        self.connect()
        result = self.connection.execute(query)
        self.connection.commit()
        return result

    def close(self):
        self.connection.close()
        self.connection = None
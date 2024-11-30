import os
import json
import logging
from crypter_db import CrypterDb
from crypter_config import CrypterConfig


class CrypterMain():
    @classmethod
    def init(cls):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        os.makedirs(configDir, exist_ok=True)
        db = CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir)
        db.setup()

    @classmethod
    def add_key(cls, keyName, userName, userPassword='112'):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        db = CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir)
        values = {'key_name': keyName, 'user_name': userName, 'user_password': userPassword}
        db.insert(tableName='records', values=values)

    @classmethod
    def get_key(cls, keyName, tableName='records'):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        db = CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir)
        return db.get(tableName=tableName, keyName=keyName)

    @classmethod
    def delete_key(cls, keyName):
        pass

    @classmethod
    def cloud_init(cls):
        pass

    @classmethod
    def cloud_sync(cls):
        pass
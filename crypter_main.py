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
import json
import random
import logging
from crypter_db import CrypterDb
from crypter_config import CrypterConfig
from crypter_token_generator import CrypterTokenGenerator


class CrypterMain():
    @classmethod
    def init(cls):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        os.makedirs(configDir, exist_ok=True)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            db.setup()
            response = db.insert("secret", {'key': CrypterTokenGenerator.generate_key()}, return_columns=['Id'])
            return cls.format_response(response, return_columns=['Id'])

    @classmethod
    def add_key(cls, keyName, userName, userPassword):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            salt = list(keyName + userName)
            random.shuffle(salt)
            userPassword = userPassword if userPassword else CrypterTokenGenerator.generate_password(''.join(salt))
            values = {'key': keyName, 'name': userName, 'password': userPassword}
            response = db.insert(tableName='records', values=values, return_columns=['key', 'name', 'password'])
            return cls.format_response(response, return_columns=['key', 'name', 'password'])

    @classmethod
    def get_key(cls, tableName='records', keyNames=None):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            response = db.get(tableName=tableName, keyNames=keyNames, return_columns=['key', 'name', 'password'])
            return cls.format_response(response, return_columns=['key', 'name', 'password'])

    @classmethod
    def delete_key(cls, tableName='records', keyNames=None):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            response = db.delete(tableName=tableName, keyNames=keyNames, return_columns=['key', 'name', 'password'])
            return cls.format_response(response, return_columns=['key', 'name', 'password'])

    @classmethod
    def format_response(cls, queryResult, return_columns):
        queryResponse = list()
        for row in queryResult:
            r = dict()
            for colName, colValue in zip(return_columns, list(row)):
                r.update({colName: colValue})
            queryResponse.append(r)
        return queryResponse

    @classmethod
    def cloud_init(cls):
        pass

    @classmethod
    def cloud_sync(cls):
        pass
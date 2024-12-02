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
import logging
from crypter_db import CrypterDb
from crypter_config import CrypterConfig
from crypter_password_generator import CrypterPasswordGenerator


class CrypterMain():
    @classmethod
    def init(cls):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        os.makedirs(configDir, exist_ok=True)
        db = CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir)
        db.setup()

    @classmethod
    def add_key(cls, keyName, userName, userPassword):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            userPassword = userPassword if userPassword else CrypterPasswordGenerator.generate_password()
            values = {'key_name': keyName, 'user_name': userName, 'user_password': userPassword}
            return cls.format_response(db.insert(tableName='records', values=values))

    @classmethod
    def get_key(cls, tableName='records', keyNames=None):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            return cls.format_response(db.get(tableName=tableName, keyNames=keyNames))

    @classmethod
    def delete_key(cls, tableName='records', keyNames=None):
        configDir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(dbName=CrypterConfig.DB_NAME, dbPath=configDir) as db:
            return cls.format_response(db.delete(tableName=tableName, keyNames=keyNames))

    @classmethod
    def format_response(cls, queryResult):
        queryResponse = list()
        for queryRow in queryResult:
            queryResponse.append({
                'keyName': queryRow[0],
                'userName': queryRow[1],
                'userPassword': queryRow[2]
            })
        return queryResponse

    @classmethod
    def cloud_init(cls):
        pass

    @classmethod
    def cloud_sync(cls):
        pass
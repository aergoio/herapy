# -*- coding: utf-8 -*-

"""Main module."""

from . import account as acc
from . import comm

from google.protobuf.json_format import MessageToJson


class Aergo:
    def __init__(self):
        self.__account = None
        self.__comm = None

    @property
    def account(self):
        return self.__account

    def new_account(self, password, private_key=None):
        self.__account = acc.Account(password, private_key)
        if private_key is not None:
            self.get_account_state(self.__account.address)
        return self.__account

    def get_account_state(self, account=None):
        if self.__comm is None:
            return None

        if account is None:
            address = self.__account.address
        else:
            address = account.address

        state = self.__comm.get_account_state(address)

        if account is None:
            self.__account.state = state
        else:
            account.state = state

        return MessageToJson(state)

    def connect(self, target):
        if target is None:
            raise ValueError('need target value')

        self.__comm = comm.Comm(target)
        self.__comm.connect()

    def disconnect(self):
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_blockchain_status(self):
        if self.__comm is None:
            return None, -1

        status = self.__comm.get_blockchain_status()
        return status.best_block_hash, status.best_height

    def get_node_accounts(self):
        result = self.__comm.get_accounts()
        accounts = []
        for a in result.accounts:
            account = acc.Account("", empty=True)
            account.address = a.address
            accounts.append(account)

        return accounts

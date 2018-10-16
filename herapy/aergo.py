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

    def create_account(self, password):
        self.__account = acc.Account(password)
        self.__account.generate_new_key()
        return self.account

    def connect(self, target):
        self.__comm = comm.Comm(target)

    def disconnect(self):
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_account_state(self, account):
        result = self.__comm.get_account_state(account)
        return MessageToJson(result)

    def get_all_accounts(self):
        result = self.__comm.get_accounts()
        accounts = []
        for account in result.accounts:
            a = acc.Account()
            a.address = account.address
            accounts.append(a)
        return accounts

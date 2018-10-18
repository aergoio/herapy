# -*- coding: utf-8 -*-

"""Main module."""

from . import account as acc
from . import comm

from google.protobuf.json_format import MessageToJson


class Aergo:
    def __init__(self, target='', private_key=b'', password=''):
        self.__target = target

        self.__account = self.__get_account(private_key, password)
        self.__comm = None

    @staticmethod
    def __get_account(private_key, password):
        if 0 == len(password):
            return None
        account = acc.Account(password)

        if 0 == len(private_key):
            account.generate_new_key()
        else:
            account.private_key = private_key

        return account

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, private_key, password):
        self.__account = self.__get_account(private_key, password)

    def create_account(self, password):
        self.__account = self.__get_account(b'', password)
        return self.account

    def connect(self, target):
        self.__comm = comm.Comm(target)

    def disconnect(self):
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_account_state(self, account):
        state = self.__comm.get_account_state(account)
        return MessageToJson(state)

    def get_blockchain_status(self):
        status = self.__comm.get_blockchain_status()
        return status.best_block_hash, status.best_height

    # TODO unnecessary functions
    '''
    def get_all_accounts(self):
        result = self.__comm.get_accounts()
        accounts = []
        for account in result.accounts:
            a = acc.Account()
            a.address = account.address
            accounts.append(a)
        return accounts
    '''

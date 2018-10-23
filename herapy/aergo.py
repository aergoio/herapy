# -*- coding: utf-8 -*-

"""Main module."""

from . import account as acc
from . import comm
from .utils.transaction import calculate_tx_hash

from google.protobuf.json_format import MessageToJson

# For PyDoc
__all__ = ['account', 'create_account', 'connect', 'disconnect', 'get_account_state', 'get_all_accounts', 'get_tx', 'sign_tx', 'send_tx', 'commit_tx']

class Aergo:
    def __init__(self):
        self.__account = None
        self.__comm = None

    @property
    def account(self):
        """
        Returns the account.
        :return:
        """
        return self.__account

    def create_account(self, password):
        """
        :param password:
        :return:
        """
        self.__account = acc.Account(password)
        self.__account.generate_new_key()
        return self.account

    def connect(self, target):
        self.__comm = comm.Comm(target)

    def disconnect(self):
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_account_state(self, account):
        if self.__comm:
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

    def get_tx(self, tx_hash):
        return self.__comm.get_tx(tx_hash)

    def sign_tx(self, tx):
        # TODO is this logic in accounts now?
        pass

    def send_tx(self, tx):
        return self.__comm.send_tx(tx)

    def commit_tx(self, tx):
        return self.__comm.commit_tx(tx)

    def get_peers(self):
        return self.__comm.get_peers()


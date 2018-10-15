# -*- coding: utf-8 -*-

"""Main module."""

from . import account


class Aergo:
    def __init__(self):
        self.__account = None

    @property
    def account(self):
        return self.__account

    def create_account(self, password):
        self.__account = account.Account(password)
        self.__account.generate_private_key()
        return self.account

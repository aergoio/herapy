# -*- coding: utf-8 -*-

"""Main module."""

from herapy.account import account
from herapy.transaction import transaction


class Herapy:
    def __init__(self):
        self._account = account.Account()
        self.address = self._account.address

    # Accounts
    def create_address(self, address):
        #print(address, len(address))
        #assert len(address) == 64
        return address

    def get_addresses(self):
        pass

    def sign_transaction(self, transaction):
        pass

    def send_unsigned_transaction(self, transaction):
        pass

    def send_signed_transaction(self, transaction):
        pass
        
    # Blockchain
    def get_transaction(self, hash):
        pass
    
    def get_block_info_by_hash(self, hash):
        pass
        
    def get_block_info_by_number(self, number):
        pass
        
    def best_block_hash(self, mode):
        pass
        
    def best_block_number(self, mode):
        pass

    def get_account_nonce(self, account):
        pass

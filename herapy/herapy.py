# -*- coding: utf-8 -*-

"""Main module."""

from herapy.network import connection_manager
from herapy.account import account
from herapy.transaction import transaction

class Herapy:
    def __init__(self):
        self.connection = connection_manager.ConnectionManager() # Manages the gRPC connection.
        transaction.Transaction()
        pass

    # Accounts
    def create_address(self, address):
        pass

    def get_addresses(self):
        pass

    def sign_transaction(self, transaction):
        private_key = self.account.private_key # OK for this to be an accessor? Security? Don't need to do anything crazy like encrypt/decrypt in memory or something.
        transaction.sign(private_key)

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

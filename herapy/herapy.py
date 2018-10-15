# -*- coding: utf-8 -*-

"""Main module."""


from herapy.comm.comm import Comm


class Herapy:
    def __init__(self, target):
        self._account = Account()
        self.address = self._account.address
        self.comm = Comm(target)

    # RPC call to create an account (note that this does not handle the public/private keys.)
    def create_account(self, passphrase):
        #return self.comm.create_account(passphrase)
        return Account()

    # Account-related methods that manage the private and public keys.
    def save_keys(self, keyname):
        self._account.km.save_keys(keyname)

    def load_keys(self, keyname):
        self._account.km.load_keys(keyname)

    def delete_keys(self, keyname):
        self._account.km.delete_keys(keyname)

    # Blockchain-related methods that query the blockchain for info.
    def get_blockchain_status(self):
        return self.comm.get_blockchain_status()

    def get_addresses(self):
        return self.comm.get_accounts()

    def get_block_info_by_hash(self, block_hash=None, block_height=0):
        return self.comm.get_block(block_hash=block_hash, block_height=block_height)

    def get_transaction(self, tx_hash):
        return self.comm.get_tx(tx_hash)

    def get_peers(self):
        return self.comm.get_peers()

"""


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
"""
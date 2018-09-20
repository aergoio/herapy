from os import mkdir
from uuid import uuid4
from herapy.utils.key_manager import KeyManager

from herapy.transaction import transaction

# WIP - this will need to store some persistent state somehow - not much data to keep track of so flat files?

class Account:
    def __init__(self):
        self.address = None
        self.balance = None
        self.nonce = None
        self.km = KeyManager()

    def sign_transaction(self, transaction):
        transaction.sign_with_key_manager(self.km)

    def send_signed_transaction(self, transaction):
        assert transaction.is_signed()
        pass

    def send_unsigned_transaction(self):
        pass

    def _send_transaction(self, address):
        self.nonce += 1


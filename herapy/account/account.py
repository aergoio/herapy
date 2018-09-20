from os import mkdir
from uuid import uuid4
from herapy.utils.key_manager import KeyManager

from herapy.transaction import transaction

class Account:
    def __init__(self):
        self.address = 0x0
        self.balance = 0
        self.nonce = 0
        self.km = KeyManager()

    def sign_transaction(self, transaction):
        transaction.sign_with_key_manager(self.km)

    def send_signed_transaction(self, transaction, address):
        assert transaction.is_signed()
        self._send_transaction(address)

    def send_unsigned_transaction(self, address):
        self._send_transaction(address)

    def _send_transaction(self, address):
        self.nonce += 1

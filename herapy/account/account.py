from os import mkdir
from uuid import uuid4
from herapy.utils.key_manager import KeyManager
from herapy.errors import InsufficientBalanceError

from herapy.transaction import transaction

class Account:
    def __init__(self):
        self.address = 0x0
        self.balance = 0
        self.nonce = 0
        self.km = KeyManager()

    def sign_transaction(self, transaction):
        transaction.sign_with_key_manager(self.km)

    def send_signed_transaction(self, transaction, to_address):
        assert transaction.is_signed()
        self._send_transaction(to_address)

    def send_unsigned_transaction(self, to_address):
        self._send_transaction(to_address)

    def _send_transaction(self, to_address):
        tx = transaction.Transaction()
        tx.from_address = self.address
        tx.to_address = to_address
        if tx.amount > self.balance:
            error = f"Cannot send transaction {tx.hash}. The amount is {amount} but you have only {self.balance} in your account."
            raise InsufficientBalanceError(error)
        self.nonce += 1
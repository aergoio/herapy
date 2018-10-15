# -*- coding: utf-8 -*-

import ecdsa
import base58

from herapy.utils.key_manager import KeyManager
from herapy.errors import InsufficientBalanceError

from herapy.transaction import transaction


class Account:
    def __init__(self, secret_key):
        self._secret_key = secret_key

    def __init__(self):
        self._generate_new_private_key()

        self.address = 0x0
        self.balance = 0
        self.nonce = 0
        self.km = KeyManager()

    def _generate_new_private_key(self):
        self._secret_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        print("Secret Key = {}".format(self._secret_key))
        print("base58(Secret Key) = {}".format(base58.b58encode_check(self._secret_key)))

    def get_private_key(self):
        return base58.b58encode_check(self._secret_key)

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
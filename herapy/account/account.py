from os import mkdir
from uuid import uuid4
from herapy.utils.key_manager import KeyManager

# WIP - this will need to store some persistent state somehow - not much data to keep track of so flat files?

class Account:
    def __init__(self):
        self.address = 0
        self.balance = 0
        self.nonce = 0
        self.key_manager = KeyManager()
        self.key_manager.generate_and_save_keys("ecdsa")

    # def load(filename):

    def create(self):
        id = uuid4().hex
        mkdir(id)

    def send_transaction(self, address):
        self.nonce += 1

    def send_signed_transaction(self):
        pass

    def send_unsigned_transaction(self):
        pass

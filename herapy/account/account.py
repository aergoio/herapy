from herapy.utils.key_manager import KeyManager

class Account:
    def __init__(self):
        self.balance = 0
        self.key_manager = KeyManager()

    def sign(self, transaction):
        pass

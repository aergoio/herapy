class Account:
    def __init__(self, private_key, nonce, balance=0):
        self.private_key = private_key
        self.nonce = nonce
        self.balance = balance

    def sign(self, transaction):
        pass


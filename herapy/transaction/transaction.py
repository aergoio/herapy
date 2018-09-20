"""
transaction = {
    hash : byte of base64
    nonce : uint
    from : byte of base58
    to : byte of base58
    amount : uint
    payload : byte of base64
    sign : byte of base64
    type : int
}
"""

class Transaction:
    # def __init__(self, hash, nonce, from_address, to_address, amount, payload, sign, type):
    def __init__(self, payload):
        self.payload = payload
        self.signature = None

        self._signed = False

    def sign_with_key_manager(self, km):
        self.signature = km.sign_message(self.payload)
        self.mark_signed()

    def mark_signed(self):
        self._signed = True


    def is_signed(self):
        return self._signed and self.signature is not None


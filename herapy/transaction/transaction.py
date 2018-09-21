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
    def __init__(self, hash, nonce, from_address, to_address, amount, payload, type):
        self.hash = hash
        self.nonce = nonce
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.payload = payload
        self.type = type

        self.signature = None
        self._signed = False

    def sign_with_key_manager(self, km):
        self.signature = km.sign_message(self.concatenate_fields())
        self._mark_signed()

    def is_signed(self):
        return self._signed and self.signature is not None

    def concatenate_fields(self):
        return self.hash + str(self.nonce) + self.from_address + self.to_address + str(self.amount) + self.payload + self.type

    def _mark_signed(self):
        self._signed = True

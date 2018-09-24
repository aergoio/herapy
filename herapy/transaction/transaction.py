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
    # TODO assert types???
    def __init__(self, hash, nonce, from_address, to_address, amount, payload, signature, type):
        self.hash = hash
        self.nonce = nonce
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.payload = payload
        self.signature = signature
        self.type = type

        # Check types. Not very Pythonic but important to get this right
        # TODO check more types
        assert isinstance(self.from_address, bytes)
        assert isinstance(self.to_address, bytes)
        assert isinstance(self.amount, int)
        assert isinstance(self.payload, bytes)
        assert isinstance(self.type, int) # TODO: can we constrain this value further? What do the int values mean?

        # self.signature = None
        # self._signed = False

    # def sign_with_key_manager(self, km):
    #     self.signature = km.sign_message(self.concatenate_fields())
    #     self._mark_signed()
    #
    # def is_signed(self):
    #     return self._signed and self.signature is not None
    #
    # def concatenate_fields(self):
    #     return self.hash + str(self.nonce) + self.from_address + self.to_address + str(self.amount) + self.payload + self.type
    #
    # def _mark_signed(self):
    #     self._signed = True

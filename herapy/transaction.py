class Transaction:
    """
    Transaction data structure:
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

    def __init__(self, hash, nonce, from_address, to_address, amount, payload, signature, type):
        self.__hash = hash
        self.__nonce = nonce
        self.__from_address = from_address
        self.__to_address = to_address
        self.__amount = amount
        self.__payload = payload
        self.__signature = signature
        self.__type = type

    @property
    def hash(self):
        return self.__hash

    @property
    def nonce(self):
        return self.__nonce

    @property
    def from_address(self):
        return self.__from_address

    @property
    def to_address(self):
        return self.__to_address

    @property
    def amount(self):
        return self.__amount


    @property
    def payload(self):
        return self.__payload

    @property
    def signature(self):
        return self.__signature

    @property
    def type(self):
        return self.__type

    def concatenate_fields(self):
        return "".join([self.hash(),
                        str(self.nonce()),
                        self.from_address(),
                        self.to_address(),
                        str(self.amount()),
                        self.payload(),
                        self.type()])

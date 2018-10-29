import hashlib

from herapy.grpc import blockchain_pb2

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

    def __init__(self, hash, nonce, from_address, to_address, amount, payload, signature, type, limit, price):
        self.__hash = hash
        self.__nonce = nonce
        self.__from_address = from_address
        self.__to_address = to_address
        self.__amount = amount
        self.__payload = payload
        self.__signature = signature
        self.__type = type
        self.__limit = limit
        self.__price = price

    def to_tx(self):
        tx_body = blockchain_pb2.TxBody(nonce=self.__nonce,
                                     account=self.__from_address,
                                     recipient=self.__to_address,
                                     amount=self.__amount,
                                     payload=self.__payload,
                                     limit=self.__limit,
                                     price=self.__price,
                                     type=self.__type,
                                     sign=self.__signature)
        tx = blockchain_pb2.Tx(body=tx_body)
        tx.hash = Transaction.calculate_tx_hash(tx)
        return tx

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

    @property
    def price(self):
        return self.__price

    @property
    def limit(self):
        return self.__limit

    @staticmethod
    def calculate_tx_hash(tx):
        m = hashlib.sha256()
        tx_bytes = tx.body.nonce.to_bytes(8, byteorder='little')
        m.update(tx_bytes)
        m.update(tx.body.account)
        m.update(tx.body.recipient)
        tx_bytes = tx.body.amount.to_bytes(8, byteorder='little')
        m.update(tx_bytes)
        m.update(tx.body.payload)
        tx_bytes = tx.body.limit.to_bytes(8, byteorder='little')
        m.update(tx_bytes)
        tx_bytes = tx.body.price.to_bytes(8, byteorder='little')
        m.update(tx_bytes)
        tx_bytes = tx.body.type.to_bytes(4, byteorder='little')
        m.update(tx_bytes)
        m.update(tx.body.sign)
        return m.digest()


# -*- coding: utf-8 -*-

"""Transaction class."""

import hashlib
import base58

from . import tx_hash as th
from ..obj import aer
from ..grpc import blockchain_pb2


class Transaction:
    """
    Transaction data structure:
    transaction = {
        hash : byte of base64
        nonce : int
        from : byte of base58
        to : byte of base58
        amount : uint
        payload : byte of base64
        sign : byte of base64
        type : int
    }
    """

    FEE_MIN_PRICE = 1
    FEE_MIN_LIMIT = 1

    TX_TYPE_NORMAL = blockchain_pb2.NORMAL
    TX_TYPE_GOVERNANCE = blockchain_pb2.GOVERNANCE

    def __init__(self, from_address=None, to_address=None,
                 nonce=0, amount=0, payload=None,
                 fee_price=FEE_MIN_PRICE, fee_limit=FEE_MIN_LIMIT):
        self.__from_address = from_address
        self.__to_address = to_address
        self.__nonce = nonce
        self.__amount = aer.Aer(amount)
        self.__payload = payload
        self.__fee_price = fee_price
        self.__fee_limit = fee_limit
        self.__sign = None
        self.__tx_type = self.TX_TYPE_NORMAL

    def calculate_hash(self, including_sign=True):
        m = hashlib.sha256()
        # nonce
        b = self.__nonce.to_bytes(8, byteorder='little')
        m.update(b)
        # from
        m.update(self.__from_address)
        # to
        if self.__to_address is not None:
            m.update(self.__to_address)
        # amount
        #b = self.__amount.to_bytes(8, byteorder='big')
        b = bytes(self.__amount)
        m.update(b)
        # payload
        if self.__payload is None:
            m.update(b'')
        else:
            m.update(self.__payload)
        # fee: limit
        b = self.__fee_limit.to_bytes(8, byteorder='little')
        m.update(b)
        # fee: price
        b = self.__fee_price.to_bytes(8, byteorder='big')
        m.update(b)
        # type
        b = self.__tx_type.to_bytes(4, byteorder='little')
        m.update(b)
        # sign
        if including_sign and self.__sign is not None:
            m.update(self.__sign)

        return m.digest()

    @property
    def nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, v):
        self.__nonce = v

    @property
    def from_address(self):
        return self.__from_address

    @from_address.setter
    def from_address(self, v):
        self.__from_address = v

    @property
    def to_address(self):
        return self.__to_address

    @to_address.setter
    def to_address(self, v):
        self.__to_address = v

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, v):
        self.__amount = aer.Aer(v)

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, v):
        self.__payload = v

    @property
    def payload_str(self):
        if self.__payload is None:
            return None
        return base58.b58encode(self.__payload).decode('utf-8')

    @property
    def fee_limit(self):
        return self.__fee_limit

    @fee_limit.setter
    def fee_limit(self, v):
        self.__fee_limit = v

    @property
    def fee_price(self):
        return self.__fee_price

    @fee_price.setter
    def fee_price(self, v):
        self.__fee_price = v

    @property
    def tx_type(self):
        return self.__tx_type

    @tx_type.setter
    def tx_type(self, v):
        if v != self.TX_TYPE_NORMAL \
                or v != self.TX_TYPE_GOVERNANCE:
            return

        self.__tx_type = v

    @property
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, v):
        self.__sign = v

    @property
    def sign_str(self):
        if self.__sign is None:
            return None
        return base58.b58encode(self.__sign).decode('utf-8')

    @property
    def tx_hash(self):
        return th.TxHash(self.calculate_hash())

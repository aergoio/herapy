# -*- coding: utf-8 -*-

"""Transaction class."""

import enum
import hashlib
import json

from . import tx_hash as txh
from ..obj import aer
from ..grpc import blockchain_pb2
from ..utils.encoding import encode_signature, decode_signature, encode_payload


@enum.unique
class TxType(enum.Enum):
    NORMAL = blockchain_pb2.NORMAL
    GOVERNANCE = blockchain_pb2.GOVERNANCE


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
        type : int
        chain_id : bytes
        sign : byte of base64
    }
    """

    def __init__(self, from_address=None, to_address=None,
                 nonce=0, amount=0, payload=None, fee_price=0, fee_limit=0,
                 read_only=False, tx_hash=None, tx_sign=None, tx_type=TxType.NORMAL,
                 chain_id=None, block=None, index_in_block=-1, is_in_mempool=False):
        self.__from_address = from_address
        self.__to_address = to_address
        self.__nonce = nonce
        self.__amount = aer.Aer(amount)
        self.__payload = payload
        if isinstance(fee_price, bytes):
            fee_price = int.from_bytes(fee_price, byteorder='big')
        self.__fee_price = aer.Aer(fee_price)
        if isinstance(fee_limit, bytes):
            fee_limit = int.from_bytes(fee_limit, byteorder='little')
        self.__fee_limit = fee_limit
        if isinstance(tx_type, bytes):
            tx_type = int.from_bytes(tx_type, byteorder='little')
        self.__tx_type = TxType(tx_type)
        self.__read_only = read_only
        self.__tx_hash = txh.TxHash(tx_hash)
        if isinstance(tx_sign, str):
            tx_sign = decode_signature(tx_sign)
        self.__sign = tx_sign

        self.__chain_id = chain_id

        self.__is_in_mempool = is_in_mempool
        if is_in_mempool:
            self.__block = None
            self.__index_in_block = -1
        else:
            self.__block = block
            self.__index_in_block = index_in_block

    def calculate_hash(self, including_sign=True):
        m = hashlib.sha256()
        # nonce
        b = self.__nonce.to_bytes(8, byteorder='little')
        m.update(b)
        # from
        m.update(bytes(self.__from_address))
        # to
        if self.__to_address is not None:
            m.update(bytes(self.__to_address))
        # amount
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
        b = bytes(self.__fee_price)
        m.update(b)
        # type
        b = self.__tx_type.value.to_bytes(4, byteorder='little')
        m.update(b)
        # chainIdHash
        m.update(self.__chain_id)
        # sign
        if including_sign and self.__sign is not None:
            m.update(self.__sign)

        return m.digest()

    @property
    def block(self):
        return self.__block

    @property
    def index_in_block(self):
        return self.__index_in_block

    @property
    def is_in_mempool(self):
        return self.__is_in_mempool

    @property
    def nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, v):
        if self.__read_only:
            return

        self.__nonce = v

    @property
    def from_address(self):
        return self.__from_address

    @from_address.setter
    def from_address(self, v):
        if self.__read_only:
            return

        self.__from_address = v

    @property
    def to_address(self):
        return self.__to_address

    @to_address.setter
    def to_address(self, v):
        if self.__read_only:
            return

        self.__to_address = v

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, v):
        if self.__read_only:
            return

        self.__amount = aer.Aer(v)

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, v):
        if self.__read_only:
            return

        self.__payload = v

    @property
    def payload_str(self):
        if self.__payload is None:
            return None
        return encode_payload(self.__payload)

    @property
    def fee_limit(self):
        return self.__fee_limit

    @fee_limit.setter
    def fee_limit(self, v):
        if self.__read_only:
            return

        self.__fee_limit = v

    @property
    def fee_price(self):
        return self.__fee_price

    @fee_price.setter
    def fee_price(self, v):
        if self.__read_only:
            return

        self.__fee_price = v

    @property
    def tx_type(self):
        return self.__tx_type

    @tx_type.setter
    def tx_type(self, v):
        if self.__read_only:
            return

        self.__tx_type = TxType(v)

    @property
    def chain_id(self):
        return self.__chain_id

    @chain_id.setter
    def chain_id(self, v):
        if self.__read_only:
            return

        self.__chain_id = v

    @property
    def sign(self):
        return self.__sign

    @sign.setter
    def sign(self, v):
        if self.__read_only:
            return

        self.__sign = v

    @property
    def sign_str(self):
        if self.__sign is None:
            return None
        return encode_signature(self.__sign)

    @property
    def tx_hash(self):
        if self.__read_only:
            return self.__tx_hash
        return txh.TxHash(self.calculate_hash())

    def json(self, without_block=False):
        tx_json = {
            "Hash": str(self.tx_hash),
            "Body": {
                "Nonce": self.nonce,
                "Account": str(self.from_address) if self.from_address is not None else None,
                "Recipient": str(self.to_address) if self.to_address is not None else None,
                "Amount": str(self.amount),
                "Payload": self.payload_str,
                "Limit": self.fee_limit,
                "Price": str(self.fee_price),
                "Sign": self.sign_str,
                "Type": self.tx_type.name,
            },
            "IsInMempool": self.__is_in_mempool,
            "IndexInBlock": self.__index_in_block,
        }

        if not without_block:
            tx_json["Block"] = self.__block.json(header_only=True) if self.__block is not None else None,

        return tx_json

    def __str__(self):
        return json.dumps(self.json(), indent=2)

    def __bytes__(self):
        return self.tx_hash
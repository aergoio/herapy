# -*- coding: utf-8 -*-

import json
import datetime

from .address import Address
from .block_hash import BlockHash
from .transaction import Transaction
from ..utils.encoding import encode_b58, encode_address
from ..utils.converter import get_hash


class Block:
    def __init__(self, hash_value=None, height=None, grpc_block=None,
                 grpc_block_header=None, tx_cnt=0, size=0):
        if grpc_block is not None:
            self._map_grpc_block(grpc_block)
        elif grpc_block_header is not None:
            if hash_value is None:
                raise ValueError("Cannot set without a block hash value")

            # block hash
            if type(hash_value) is not BlockHash:
                hash_value = BlockHash(hash_value)
            self.__hash = hash_value
            # header
            self._map_grpc_block_header(grpc_block_header)
            # body
            self.__tx_list = []
            self.__tx_cnt = tx_cnt
            self.__size = size
        else:
            if hash_value is None:
                raise ValueError("Cannot set without a block hash value")

            # block hash
            if type(hash_value) is not BlockHash:
                hash_value = BlockHash(hash_value)
            self.__hash = hash_value
            # header
            self.__chain_id = None
            self.__prev_block = None
            self.__height = height
            self.__timestamp = None
            self.__blocks_root_hash = None
            self.__txs_root_hash = None
            self.__receipts_root_hash = None
            self.__confirms = None
            self.__public_key = None
            self.__sign = None
            self.__coinbase_account = None
            # body
            self.__tx_list = []
            self.__tx_cnt = tx_cnt
            self.__size = size

    def _map_grpc_block_header(self, header):
        # header
        self.__chain_id = header.chainID
        if header.blockNo > 0:
            self.__prev_block = Block(hash_value=header.prevBlockHash,
                                      height=header.blockNo - 1)
        else:
            self.__prev_block = None
        self.__height = header.blockNo
        self.__timestamp = header.timestamp
        self.__blocks_root_hash = header.blocksRootHash
        self.__txs_root_hash = header.txsRootHash
        self.__receipts_root_hash = header.receiptsRootHash
        self.__confirms = header.confirms
        self.__public_key = header.pubKey
        self.__sign = header.sign
        self.__coinbase_account = header.coinbaseAccount

    def _map_grpc_block(self, v):
        self.__hash = BlockHash(v.hash)
        # header
        self._map_grpc_block_header(v.header)
        # body
        self.__tx_list = []
        for i, tx in enumerate(v.body.txs):
            from_address = Address(None, empty=True)
            from_address.value = tx.body.account
            to_address = Address(None, empty=True)
            to_address.value = tx.body.recipient

            block_tx = Transaction(read_only=True, tx_hash=tx.hash,
                                   nonce=tx.body.nonce,
                                   from_address=from_address,
                                   to_address=to_address,
                                   amount=tx.body.amount,
                                   payload=tx.body.payload,
                                   gas_price=tx.body.gasPrice,
                                   gas_limit=tx.body.gasLimit,
                                   tx_sign=tx.body.sign, tx_type=tx.body.type,
                                   block=self, index_in_block=i,
                                   is_in_mempool=False)
            self.__tx_list.append(block_tx)
        self.__tx_cnt = len(self.__tx_list)
        self.__size = v.ByteSize()

    @property
    def hash(self):
        return self.__hash

    @property
    def chain_id(self):
        return self.__chain_id

    @property
    def chain_id_hash(self):
        if self.__chain_id is None:
            return None
        return get_hash(self.__chain_id, no_rand=True, no_encode=True)

    @property
    def chain_id_hash_b58(self):
        if self.__chain_id is None:
            return None
        return get_hash(self.__chain_id, no_rand=True, no_encode=False)

    @property
    def height(self):
        return self.__height

    @property
    def prev(self):
        return self.__prev_block

    @property
    def block_no(self):
        return self.height

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def datetimestamp(self):
        if self.__timestamp is None:
            return None

        return str(datetime.datetime.fromtimestamp(self.timestamp // 1000000000))

    @property
    def blocks_root_hash(self):
        return self.__blocks_root_hash

    @property
    def txs_root_hash(self):
        return self.__txs_root_hash

    @property
    def receipts_root_hash(self):
        return self.__receipts_root_hash

    @property
    def confirms(self):
        return self.__confirms

    @property
    def public_key(self):
        return self.__public_key

    @property
    def sign(self):
        return self.__sign

    @property
    def coinbase_account(self):
        return self.__coinbase_account

    @property
    def tx_list(self):
        return self.__tx_list

    @property
    def num_of_tx(self):
        return self.__tx_cnt

    @property
    def size(self):
        return self.__size

    def get_tx(self, index):
        return self.__tx_list[index]

    def json(self, header_only=False):
        body_json = {
            "hash": str(self.hash),
            "header": {
                "chain_id": self.chain_id_hash_b58,
                "previous_block_hash": str(self.prev.hash) if self.prev is not None else None,
                "block_no": self.block_no,
                "timestamp": self.timestamp,
                "datetimestamp": self.datetimestamp,
                "blocks_root_hash": encode_b58(self.blocks_root_hash),
                "txs_root_hash": encode_b58(self.txs_root_hash),
                "receipts_root_hash": encode_b58(self.receipts_root_hash),
                "confirms": self.confirms,
                "pub_key": encode_b58(self.public_key) if self.public_key is not None else None,
                "sign": encode_b58(self.sign),
                "coinbase_account": encode_address(self.coinbase_account) if self.coinbase_account is not None else None,
                "tx_count": self.__tx_cnt,
                "size": self.__size
            },
        }

        if not header_only:
            tx_list = []
            for tx in self.tx_list:
                tx_list.append(tx.json())

            body_json["body"] = {
                "tx_list": tx_list,
            }

        return body_json

    def __str__(self):
        return json.dumps(self.json(), indent=2)

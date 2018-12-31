# -*- coding: utf-8 -*-

import json

from .address import Address
from .block_hash import BlockHash
from .transaction import Transaction
from ..utils.encoding import encode_b58


class Block:
    def __init__(self, hash_value=None, height=None, grpc_block=None):
        if grpc_block is not None:
            self._map_grpc_block(grpc_block)
            return

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

    def _map_grpc_block(self, v):
        self.__hash = BlockHash(v.hash)
        # header
        header = v.header
        self.__chain_id = header.chainID
        self.__prev_block = Block(hash_value=header.prevBlockHash,
                                  height=header.blockNo - 1)
        self.__height = header.blockNo
        self.__timestamp = header.timestamp
        self.__blocks_root_hash = header.blocksRootHash
        self.__txs_root_hash = header.txsRootHash
        self.__receipts_root_hash = header.receiptsRootHash
        self.__confirms = header.confirms
        self.__public_key = header.pubKey
        self.__sign = header.sign
        self.__coinbase_account = header.coinbaseAccount
        # body
        self.__tx_list = []
        for tx in v.body.txs:
            self.__tx_list.append(Transaction(read_only=True, tx_hash=tx.hash, nonce=tx.body.nonce,
                                              from_address=Address(tx.body.account),
                                              to_address=Address(tx.body.recipient),
                                              amount=tx.body.amount, payload=tx.body.payload,
                                              fee_price=tx.body.price, fee_limit=tx.body.limit,
                                              tx_sign=tx.body.sign, tx_type=tx.body.type))

    @property
    def hash(self):
        return self.__hash

    @property
    def chain_id(self):
        return self.__chain_id

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

    def json(self):
        tx_list = []
        for tx in self.tx_list:
            tx_list.append(tx.json())

        return {
            "Hash": str(self.hash),
            "Header": {
                "ChainID": encode_b58(self.chain_id),
                "PreviousBlockHash": str(self.prev.hash) if self.prev is not None else None,
                "BlockNo": self.block_no,
                "Timestamp": self.timestamp,
                "BlocksRootHash": encode_b58(self.blocks_root_hash),
                "TxsRootHash": encode_b58(self.txs_root_hash),
                "ReceiptsRootHash": encode_b58(self.receipts_root_hash),
                "Confirms": self.confirms,
                "PubKey": encode_b58(self.public_key) if self.public_key is not None else None,
                "Sign": encode_b58(self.sign),
                "CoinbaseAccount": encode_b58(self.coinbase_account),
            },
            "Body": {
                "Txs": tx_list,
            },
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)

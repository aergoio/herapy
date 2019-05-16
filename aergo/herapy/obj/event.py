# -*- coding: utf-8 -*-

import json

from .block_hash import BlockHash
from .tx_hash import TxHash
from ..utils.encoding import encode_address


class Event:
    def __init__(self, grpc_event):
        self.__contract_address = encode_address(grpc_event.contractAddress)
        self.__name = grpc_event.eventName
        self.__index = grpc_event.eventIdx
        try:
            self.__args = json.loads(grpc_event.jsonArgs)
        except:
            self.__args = [grpc_event.jsonArgs]
        self.__block_hash = BlockHash(grpc_event.blockHash)
        self.__block_height = grpc_event.blockNo
        self.__tx_hash = TxHash(grpc_event.txHash)
        self.__tx_index = grpc_event.txIndex

    @property
    def tx_hash(self):
        return self.__tx_hash

    @property
    def tx_index(self):
        return self.__tx_index

    @property
    def block_hash(self):
        return self.__block_hash

    @property
    def block_height(self):
        return self.__block_height

    @property
    def contract_address(self):
        return self.__contract_address

    @property
    def index(self):
        return self.__index

    @property
    def name(self):
        return self.__name

    @property
    def arguments(self):
        return self.__args

    def json(self):
        return {
            'contract_address': self.contract_address,
            'event_name': self.name,
            'index': self.index,
            'arguments': self.arguments,
            'block_hash': str(self.block_hash),
            'block_height': self.block_height,
            'tx_hash': str(self.tx_hash),
            'tx_index': self.tx_index,
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)

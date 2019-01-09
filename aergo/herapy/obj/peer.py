# -*- coding: utf-8 -*-

import json
import socket

from google.protobuf.json_format import MessageToJson

from .block import Block
from ..status.peer_status import PeerStatus
from ..utils.encoding import encode_b58
from ..utils.converter import convert_ip_bytes_to_str


class Peer:
    def __init__(self):
        self.__info = None
        self.__address = None
        self.__port = None
        self.__id = None
        self.__state = None

    @property
    def info(self):
        return MessageToJson(self.__info)

    @info.setter
    def info(self, v):
        self.__info = v
        self.__address = convert_ip_bytes_to_str(v.address.address)
        self.__port = v.address.port
        self.__id = v.address.peerID
        self.__bestblock = Block(hash_value=v.bestblock.blockHash, height=v.bestblock.blockNo)
        self.__state = PeerStatus(v.state)

    @property
    def address(self):
        return self.__address

    @property
    def port(self):
        return self.__port

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s):
        self.__state = s

    def json(self):
        return {
            "Address": {
                "Address": str(self.__address),
                "Port": self.__port,
                "PeerID": encode_b58(self.__id),
            },
            "BestBlock": {
                "BlockNo": self.__bestblock.block_no,
                "BlockHash": str(self.__bestblock.hash),
            },
            "State": self.__state.name
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)

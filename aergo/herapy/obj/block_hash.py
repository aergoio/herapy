# -*- coding: utf-8 -*-

import base58


class BlockHash:
    def __init__(self, bh):
        if isinstance(bh, str):
            bh = BlockHash.decode_block_hash(bh)
        self.__block_hash = bh

    @property
    def value(self):
        return self.__block_hash

    def __bytes__(self):
        return self.__block_hash

    def __str__(self):
        return BlockHash.encode_block_hash(self.__block_hash)

    @staticmethod
    def encode_block_hash(b):
        return base58.b58encode(b).decode('utf-8')

    @staticmethod
    def decode_block_hash(s):
        return base58.b58decode(s)

# -*- coding: utf-8 -*-

from ..utils.encoding import encode_block_hash, decode_block_hash


class BlockHash:
    def __init__(self, bh):
        if isinstance(bh, str):
            bh = decode_block_hash(bh)
        self.__block_hash = bh

    @property
    def value(self):
        return self.__block_hash

    def __bytes__(self):
        return self.__block_hash

    def __str__(self):
        return encode_block_hash(self.__block_hash)

# -*- coding: utf-8 -*-

from ..utils.encoding import encode_tx_hash


class TxHash:
    def __init__(self, th):
        self.__tx_hash = th

    def __str__(self):
        return encode_tx_hash(self.__tx_hash)

    def __bytes__(self):
        return self.__tx_hash

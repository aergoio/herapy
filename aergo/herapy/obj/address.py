# -*- coding: utf-8 -*-

from ecdsa.ecdsa import int_to_string

from ..utils.encoding import encode_address


class Address:
    def __init__(self, pubkey):
        if pubkey is None:
            assert 1 == 0
        self.__generate_address(pubkey)

    def __str__(self):
        return encode_address(self.__address)

    def __bytes__(self):
        return self.__address

    def __generate_address(self, pubkey):
        pubkey_x = pubkey.point.x()
        x_bytes = int_to_string(pubkey_x)
        pubkey_y = pubkey.point.y()
        head = bytes([2] if 0 == pubkey_y % 2 else [3])
        self.__address = head + x_bytes

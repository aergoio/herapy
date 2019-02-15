# -*- coding: utf-8 -*-

from ecdsa.ecdsa import int_to_string

from ..utils.encoding import encode_address, decode_address


class Address:
    def __init__(self, pubkey, empty=False):
        if empty:
            self.__empty = True
            return

        if pubkey is None:
            assert 1 == 0

        if isinstance(pubkey, str):
            pubkey = decode_address(pubkey)

        if isinstance(pubkey, bytes):
            self.__address = pubkey
        else:
            self.__generate_address(pubkey)

    @property
    def value(self):
        return self.__address

    @value.setter
    def value(self, v):
        if self.__empty:
            if isinstance(v, str):
                self.__address = decode_address(v)
            elif isinstance(v, bytes):
                self.__address = v

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

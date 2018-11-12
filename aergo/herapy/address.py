# -*- coding: utf-8 -*-

import base58

from ecdsa.ecdsa import int_to_string


class Address:
    ADDRESS_BYTES_LENGTH = 33
    ADDRESS_VERSION = b'\x42'

    def __init__(self, pubkey):
        if pubkey is not None:
            self.__generate_address(pubkey)

    def __str__(self):
        return self.encode_address(self.__address)

    def __generate_address(self, pubkey):
        pubkey_x = pubkey.point.x()
        x_bytes = int_to_string(pubkey_x)
        pubkey_y = pubkey.point.y()
        head = bytes([2] if 0 == pubkey_y % 2 else [3])
        self.__address = head + x_bytes

    @staticmethod
    def encode_address(address):
        v = Address.ADDRESS_VERSION + address
        return base58.b58encode_check(v).decode('utf-8')

    @staticmethod
    def decode_address(address):
        v = base58.b58decode_check(address)
        return v[len(Address.ADDRESS_VERSION):]

    def get_address_bytes(self):
        return self.__address

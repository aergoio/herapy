# -*- coding: utf-8 -*-

import ecdsa
import hashlib
import base58

from ecdsa.ecdsa import int_to_string

PRIVATE_KEY_BYTES_LENGTH = 32
ADDRESS_BYTES_LENGTH = 33
ADDRESS_VERSION = b'\x42'


def generate_address(pubkey):
    pubkey_x = pubkey.point.x()
    x_bytes = int_to_string(pubkey_x)
    pubkey_y = pubkey.point.y()
    head = bytes([2] if 0 == pubkey_y % 2 else [3])
    return head + x_bytes


def encode_address(address):
    address_v = ADDRESS_VERSION + address
    return base58.b58encode_check(address_v).decode('utf-8')


class Account:
    def __init__(self, password):
        self.password = password
        self.__signing_key = None
        self.__private_key = None
        self.__address = None

    def generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey

    @property
    def private_key(self):
        D = self.__signing_key.privkey.secret_multiplier
        return D.to_bytes(PRIVATE_KEY_BYTES_LENGTH, byteorder='big')

    @private_key.setter
    def private_key(self, private_key):
        D = int.from_bytes(private_key, byteorder='big')
        self.__signing_key = ecdsa.SigningKey.from_secret_exponent(secexp=D,
                                                                   curve=ecdsa.SECP256k1,
                                                                   hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey

    @property
    def public_key(self):
        if self.__private_key is None:
            return None

        return self.__private_key.public_key

    @property
    def address(self):
        if self.__private_key is None:
            return None

        if self.__address is None:
            self.__address = generate_address(self.__private_key.public_key)

        return self.__address

    @property
    def address_str(self):
        if self.__address is None:
            self.address

        if self.__address is None:
            return None

        return encode_address(self.__address)


# -*- coding: utf-8 -*-

import ecdsa
import hashlib
import base58

PRIVATE_KEY_BYTES_LENGTH = 32
ADDRESS_BYTES_LENGTH = 33
ADDRESS_VERSION = b'0x42'


def int_to_string(x):
    """Convert integer x into a string of bytes, as per X9.62."""
    assert x >= 0
    if x == 0:
        return b'\0'
    result = []
    while x:
        ordinal = x & 0xFF
        result.append(ordinal.to_bytes(1, byteorder='big'))
        x >>= 8

    result.reverse()
    return b''.join(result)


def generate_address(pubkey):
    pubkey_x = pubkey.point.x()
    x_bytes = int_to_string(pubkey_x)
    pubkey_y = pubkey.point.y()
    head = bytes([2] if 0 == pubkey_y % 2 else [3])
    return head + x_bytes


def encode_address(address):
    address_v = ADDRESS_VERSION.join(address)
    return base58.b58decode_check(address_v)


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


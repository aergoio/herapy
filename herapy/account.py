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


def decode_address(address):
    address_v = base58.b58decode_check(address)
    return address_v[len(ADDRESS_VERSION):]


class Account:
    def __init__(self, password=None):
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

    def __get_address(self):
        if self.__address is None and self.__private_key is not None:
            self.__address = generate_address(self.__private_key.public_key)

    def __set_address(self, address_bytes):
        if self.__address is not None:
            self.__signing_key = None
            self.__private_key = None

        if isinstance(address_bytes, str):
            address_bytes = decode_address(address_bytes)

        self.__address = address_bytes

    @property
    def address(self):
        self.__get_address()
        return self.__address

    @address.setter
    def address(self, address_bytes):
        self.__set_address(address_bytes)

    @property
    def address_str(self):
        self.__get_address()
        return encode_address(self.__address)

    @address_str.setter
    def address_str(self, address_str):
        self.__set_address(address_str)


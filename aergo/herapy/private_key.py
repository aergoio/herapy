# -*- coding: utf-8 -*-

import ecdsa
import hashlib
import base58


class PrivateKey:
    PRIVATE_KEY_BYTES_LENGTH = 32
    PRIVATE_KEY_VERSION = b'\xAA'

    def __init__(self, pk):
        if pk is not None:
            self.__get_key(pk)
        else:
            self.__generate_new_key()

    def __str__(self):
        return self.encode_private_key(self.__get_private_key_bytes())

    def __generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey

    def __get_key(self, private_key):
        if isinstance(private_key, str):
            private_key = self.decode_private_key(private_key)

        d = int.from_bytes(private_key, byteorder='big')
        sk = ecdsa.SigningKey.from_secret_exponent(secexp=d,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)
        self.__signing_key = sk
        self.__private_key = self.__signing_key.privkey

    def __get_private_key_bytes(self):
        d = self.__private_key.secret_multiplier
        return d.to_bytes(PrivateKey.PRIVATE_KEY_BYTES_LENGTH, byteorder='big')

    @staticmethod
    def encode_private_key(private_key):
        v = PrivateKey.PRIVATE_KEY_VERSION + private_key
        return base58.b58encode_check(v).decode('utf-8')

    @staticmethod
    def decode_private_key(private_key):
        v = base58.b58decode_check(private_key)
        return v[len(PrivateKey.PRIVATE_KEY_VERSION):]

    @property
    def public_key(self):
        return self.__private_key.public_key

# -*- coding: utf-8 -*-

import ecdsa
import hashlib

from ecdsa.util import string_to_number

from . import address

from ..utils.encoding import encode_private_key, decode_private_key
from ..utils.signature import deserialize_sig, serialize_sig


class PrivateKey:
    def __init__(self, pk):
        if pk is not None:
            self.__get_key(pk)
        else:
            self.__generate_new_key()

        self.__address = address.Address(self.__private_key.public_key)

    def __str__(self):
        return encode_private_key(self.__get_private_key_bytes())

    def __bytes__(self):
        return self.__get_private_key_bytes()

    def __generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey

    def __get_singing_key_instance(self, private_key):
        d = int.from_bytes(private_key, byteorder='big')
        """
        sk = ecdsa.SigningKey.from_secret_exponent(secexp=d,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)
        """
        # to avoid 'Assert' error
        sk = ecdsa.SigningKey(_error__please_use_generate=True)
        sk.curve = ecdsa.SECP256k1
        sk.default_hashfunc = hashlib.sha256
        sk.baselen = ecdsa.SECP256k1.baselen
        pubkey_point = ecdsa.SECP256k1.generator * d
        pubkey = ecdsa.ecdsa.Public_key(ecdsa.SECP256k1.generator, pubkey_point)
        pubkey.order = ecdsa.SECP256k1.order
        sk.verifying_key = ecdsa.VerifyingKey.from_public_point(pubkey_point,
                                                                ecdsa.SECP256k1,
                                                                hashlib.sha256)
        sk.privkey = ecdsa.ecdsa.Private_key(pubkey, d)
        sk.privkey.order = ecdsa.SECP256k1.order
        return sk

    def __get_key(self, private_key):
        if isinstance(private_key, str):
            private_key = decode_private_key(private_key)

        self.__signing_key = self.__get_singing_key_instance(private_key)
        self.__private_key = self.__signing_key.privkey

    def __get_private_key_bytes(self):
        d = self.__private_key.secret_multiplier
        return d.to_bytes((d.bit_length() + 7) // 8, byteorder='big')

    def sign_msg(self, msg):
        r, s = self.__signing_key.sign_number(string_to_number(msg))
        order = self.__private_key.public_key.generator.order()
        return serialize_sig(r, s, order)

    def verify_sign(self, msg, sign):
        r, s = deserialize_sig(sign)
        signature = ecdsa.ecdsa.Signature(r, s)
        return self.__private_key.public_key.verifies(string_to_number(msg), signature)

    @property
    def public_key(self):
        return self.__private_key.public_key

    @property
    def address(self):
        return self.__address

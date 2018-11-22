# -*- coding: utf-8 -*-

import ecdsa
import hashlib

from ecdsa.util import number_to_string, string_to_number

from ..utils.encoding import encode_private_key, decode_private_key
from ..constants import PRIVATE_KEY_BYTES_LENGTH


class PrivateKey:
    def __init__(self, pk):
        if pk is not None:
            self.__get_key(pk)
        else:
            self.__generate_new_key()

    def __str__(self):
        return encode_private_key(self.__get_private_key_bytes())

    def __bytes__(self):
        return self.__get_private_key_bytes()

    def __generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey

    def __get_key(self, private_key):
        if isinstance(private_key, str):
            private_key = decode_private_key(private_key)

        d = int.from_bytes(private_key, byteorder='big')
        sk = ecdsa.SigningKey.from_secret_exponent(secexp=d,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)
        self.__signing_key = sk
        self.__private_key = self.__signing_key.privkey

    def __get_private_key_bytes(self):
        d = self.__private_key.secret_multiplier
        return d.to_bytes(PRIVATE_KEY_BYTES_LENGTH, byteorder='big')

    def __canonicalize_int(self, n, order):
        b = number_to_string(n, order)
        if (b[0] & 80) != 0:
            b = bytes([0]) + b
        return b

    def __serialize(self, r, s):
        order = self.__private_key.public_key.generator.order()
        half_order = order >> 1
        if s > half_order:
            s = order - s

        rb = self.__canonicalize_int(r, order)
        sb = self.__canonicalize_int(s, order)

        length = 4 + len(rb) + len(sb)
        b = b'\x30' + bytes([length])
        b += b'\x02' + bytes([len(rb)]) + rb
        b += b'\x02' + bytes([len(sb)]) + sb
        return b

    def __deserialize(self, sig):
        idx = 0
        if b'\x30'[0] != sig[idx]:
            # TODO error handling
            return None, None

        idx += 1

        length = len(sig) - 2
        if length != sig[idx]:
            # TODO error handling
            return None, None

        idx += 1

        # check R bytes
        if b'\x02'[0] != sig[idx]:
            # TODO error handling
            return None, None

        idx += 1
        r_len = sig[idx]
        idx += 1
        rb = sig[idx:idx+r_len]
        idx += r_len

        # check S bytes
        if b'\x02'[0] != sig[idx]:
            # TODO error handling
            return None, None

        idx += 1
        s_len = sig[idx]
        idx += 1
        sb = sig[idx:idx+s_len]

        return string_to_number(rb), string_to_number(sb)

    def sign_msg(self, msg):
        r, s = self.__signing_key.sign_number(string_to_number(msg))
        return self.__serialize(r, s)

    def verify_sign(self, msg, sign):
        r, s = self.__deserialize(sign)
        signature = ecdsa.ecdsa.Signature(r, s)
        return self.__private_key.public_key.verifies(string_to_number(msg), signature)

    @property
    def public_key(self):
        return self.__private_key.public_key

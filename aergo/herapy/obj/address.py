# -*- coding: utf-8 -*-

import ecdsa

from ..utils.encoding import encode_address, decode_address
from ..utils.signature import uncompress_key
from ..constants import *


class Address:
    def __init__(self, pubkey=None, address=None, curve=ecdsa.SECP256k1, empty=False):
        self.__curve = curve

        if empty:
            self.__public_key = None
            self.__address = None
            return

        if pubkey is None and address is None:
            assert 1 == 0

        if pubkey is not None:
            self.__public_key = self.__derive_public_key(pubkey)
            if self.__public_key is None:
                raise ValueError("public key is not proper")
            self.__generate_address()
        else:
            self.__get_public_key(address)


    @property
    def public_key(self):
        return self.__public_key

    @property
    def curve(self):
        return self.__curve

    def __str__(self):
        return encode_address(self.__address)

    def __bytes__(self):
        return self.__address

    def __derive_public_key(self, public_key, curve=ecdsa.SECP256k1):
        if isinstance(public_key, ecdsa.ecdsa.Public_key):
            return public_key

        head = public_key[:1]
        if head not in (PUBLIC_KEY_UNCOMPRESSED, PUBLIC_KEY_COMPRESSED_O, PUBLIC_KEY_COMPRESSED_E):
            # can be a smart contract address, so no error
            return None


        x_bytes = public_key[1:curve.baselen+1]
        x = ecdsa.util.string_to_number(x_bytes)

        if PUBLIC_KEY_UNCOMPRESSED == head:
            y_bytes = public_key[curve.baselen+1:]
            y = ecdsa.util.string_to_number(y_bytes)
        else:
            a = curve.curve.a()
            b = curve.curve.b()
            p = curve.curve.p()

            if ecdsa.SECP256k1 == curve:
                # source: https://stackoverflow.com/questions/43629265/deriving-an-ecdsa-uncompressed-public-key-from-a-compressed-one?rq=1
                y_square = (pow(x, 3, p) + a * x + b) % p
                y_square_square_root = pow(y_square, (p+1)//4, p)
                if ((head == PUBLIC_KEY_COMPRESSED_E and y_square_square_root & 1) or
                        (head == PUBLIC_KEY_COMPRESSED_O and not y_square_square_root & 1)):
                    y = (-y_square_square_root) % p
                else:
                    y = y_square_square_root
            else:
                # if supporting more formula, need to implement
                assert 1 == 0

        point = ecdsa.ellipticcurve.Point(curve.curve, x, y, curve.order)
        return ecdsa.ecdsa.Public_key(curve.generator, point)

    def __get_public_key(self, address):
        if isinstance(address, str):
            address = decode_address(address)
        elif not isinstance(address, bytes):
            raise TypeError('address can be only string or bytes')

        self.__public_key = self.__derive_public_key(address)
        if self.__public_key is None:
            self.__address = address
        else:
            self.__generate_address()

    def __generate_address(self):
        x = self.__public_key.point.x()
        x_bytes = ecdsa.util.number_to_string(x, self.__curve.order)

        y = self.__public_key.point.y()
        head = PUBLIC_KEY_COMPRESSED_E if 0 == y % 2 else PUBLIC_KEY_COMPRESSED_O

        self.__address = head + x_bytes

    def get_public_key(self, compressed=True):
        if compressed:
            if 0 == self.__public_key.point.y() % 2:
                v = PUBLIC_KEY_COMPRESSED_E
            else:
                v = PUBLIC_KEY_COMPRESSED_O
            v += ecdsa.util.number_to_string(self.__public_key.point.x(),
                                             self.__curve.order)
        else:
            v = PUBLIC_KEY_UNCOMPRESSED
            v += ecdsa.util.number_to_string(self.__public_key.point.x(),
                                             self.__curve.order)
            v += ecdsa.util.number_to_string(self.__public_key.point.y(),
                                             self.__curve.order)
        return v

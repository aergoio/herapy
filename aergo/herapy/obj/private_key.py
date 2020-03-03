# -*- coding: utf-8 -*-

import ecdsa
import hashlib

from ecdsa.util import string_to_number
from typing import (
    Union,
)

from .address import Address

from ..utils.encryption import (
    encrypt_bytes,
    decrypt_bytes
)
from ..utils.encoding import (
    encode_private_key,
    decode_private_key,
    encode_b58,
    decode_b58
)
from ..utils.signature import (
    deserialize_sig,
    serialize_sig
)
from ..errors.general_exception import (
    GeneralException
)


DEFAULT_CURVE = ecdsa.SECP256k1


class PrivateKey:
    def __init__(
        self,
        pk: Union[str, bytes, None]
    ) -> None:
        if pk is not None:
            self.__get_key(pk)
        else:
            self.__generate_new_key()

        self.__address = Address(self.__private_key.public_key)

    def __str__(self) -> str:
        privkey = encode_private_key(self.__get_private_key_bytes())
        assert privkey
        return privkey

    def __bytes__(self) -> bytes:
        return self.__get_private_key_bytes()

    def __generate_new_key(self) -> None:
        self.__signing_key = ecdsa.SigningKey.generate(curve=DEFAULT_CURVE,
                                                       hashfunc=hashlib.sha256)
        self.__signing_key.get_verifying_key()
        self.__private_key = self.__signing_key.privkey

    def __get_singing_key_instance(
        self,
        private_key: bytes
    ) -> ecdsa.SigningKey:
        if len(private_key) > 32:   # if over default size,
            # check bytes head
            if private_key[:4] != "\x08\x02\x12\x20".encode("latin-1"):
                raise ValueError("private key is incorrect")
            else:
                private_key = private_key[4:]

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
        pubkey = ecdsa.ecdsa.Public_key(
            ecdsa.SECP256k1.generator, pubkey_point)
        pubkey.order = ecdsa.SECP256k1.order
        sk.verifying_key = ecdsa.VerifyingKey.from_public_point(
            pubkey_point, ecdsa.SECP256k1, hashlib.sha256)
        sk.privkey = ecdsa.ecdsa.Private_key(pubkey, d)
        sk.privkey.order = ecdsa.SECP256k1.order
        return sk

    def __get_key(
        self,
        private_key: Union[str, bytes]
    ) -> None:
        if isinstance(private_key, str):
            privkey = decode_private_key(private_key)
            assert privkey  # for mypy Optional[bytes] -> bytes
            private_key = privkey

        self.__signing_key = self.__get_singing_key_instance(private_key)
        self.__private_key = self.__signing_key.privkey

    def __get_private_key_bytes(self) -> bytes:
        d = self.__private_key.secret_multiplier
        return d.to_bytes((d.bit_length() + 7) // 8, byteorder='big')

    def sign_msg(self, msg: bytes) -> bytes:
        r, s = self.__signing_key.sign_number(string_to_number(msg))
        order = self.__private_key.public_key.generator.order()
        return serialize_sig(r, s, order)

    def verify_sign(self, msg: bytes, sign: bytes) -> bool:
        r, s = deserialize_sig(sign)
        signature = ecdsa.ecdsa.Signature(r, s)
        return self.__private_key.public_key.verifies(
            string_to_number(msg), signature)

    def __get_multiplied_point(
        self,
        address: Union[str, Address]
    ) -> ecdsa.ellipticcurve.Point:

        if isinstance(address, str):
            address = Address(address, curve=DEFAULT_CURVE)

        opponent_pubkey = address.public_key
        if not opponent_pubkey:
            raise GeneralException("Address object must have a public key")
        return opponent_pubkey.point * self.__private_key.secret_multiplier

    def asymmetric_encrypt_msg(
        self,
        address: Union[str, Address],
        msg: Union[str, bytes]
    ) -> str:
        if isinstance(msg, str):
            msg = bytes(msg, encoding='utf-8')

        point = self.__get_multiplied_point(address)
        password = point.x() + point.y()
        password = password.to_bytes((password.bit_length() + 7) // 8,
                                     byteorder='big')

        enc_msg = encode_b58(encrypt_bytes(msg, password))
        assert enc_msg  # for mypy Optional[str] -> str
        return enc_msg

    def asymmetric_decrypt_msg(
        self,
        address: Union[str, Address],
        enc_msg: Union[str, bytes]
    ) -> bytes:
        if isinstance(enc_msg, str):
            enc_bytes = decode_b58(enc_msg)
            assert enc_bytes  # for mypy Optional[bytes] -> bytes
            enc_msg = enc_bytes

        point = self.__get_multiplied_point(address)
        password = point.x() + point.y()
        password = password.to_bytes((password.bit_length() + 7) // 8,
                                     byteorder='big')

        return decrypt_bytes(enc_msg, password)

    @property
    def public_key(self) -> ecdsa.ecdsa.Public_key:
        return self.__private_key.public_key

    @property
    def address(self) -> Address:
        return self.__address

    def get_signing_key(self) -> ecdsa.keys.SigningKey:
        return self.__signing_key

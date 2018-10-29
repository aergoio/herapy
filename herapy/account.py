# -*- coding: utf-8 -*-

import ecdsa
import hashlib
import base58

from ecdsa.ecdsa import int_to_string
from google.protobuf.json_format import MessageToJson


class Account:
    PRIVATE_KEY_BYTES_LENGTH = 32
    PRIVATE_KEY_VERSION = b'\xAA'
    ADDRESS_BYTES_LENGTH = 33
    ADDRESS_VERSION = b'\x42'

    def __init__(self, password, private_key=None, empty=False):
        if empty:
            self.__private_key = None
            self.__signing_key = None
            self.__address = None
            self.__state = None
            return

        self.password = password

        if private_key is None:
            self.__generate_new_key()
        else:
            self.__get_key(private_key)

        self.__state = None

    def sign_message(self, message):
        return self.__signing_key.sign(message, hashfunc=hashlib.sha256)

    def __generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey
        self.__address = Account.generate_address(self.__private_key.public_key)

    def __get_key(self, private_key):
        if isinstance(private_key, str):
            private_key = Account.decode_private_key(private_key)

        D = int.from_bytes(private_key, byteorder='big')
        sk = ecdsa.SigningKey.from_secret_exponent(secexp=D,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)
        self.__signing_key = sk
        self.__private_key = self.__signing_key.privkey
        self.__address = Account.generate_address(self.__private_key.public_key)

    def __get_private_key_bytes(self):
        D = self.__private_key.secret_multiplier
        return D.to_bytes(Account.PRIVATE_KEY_BYTES_LENGTH, byteorder='big')

    @property
    def private_key(self):
        return self.__get_private_key_bytes()

    @property
    def private_key_str(self):
        return Account.encode_private_key(self.__get_private_key_bytes())

    @property
    def public_key(self):
        if self.__private_key is None:
            return None

        return self.__private_key.public_key

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, v):
        if self.__address is not None:
            raise ValueError('not empty account')

        if isinstance(v, str):
            v = Account.decode_address(v)
        self.__address = v

    @property
    def address_str(self):
        return Account.encode_address(self.__address)

    @property
    def state(self):
        if self.__state is None:
            return None
        return MessageToJson(self.__state)

    @state.setter
    def state(self, v):
        self.__state = v

    @property
    def nonce(self):
        if self.__state is None:
            return 0
        return self.__state.nonce

    @property
    def balance(self):
        if self.__state is None:
            return 0
        return self.__state.balance

    @property
    def code_hash(self):
        if self.__state is None:
            return None
        return self.__state.codeHash

    @property
    def storage_root(self):
        if self.__state is None:
            return None
        return self.__state.storageRoot

    @property
    def sql_recovery_point(self):
        if self.__state is None:
            return None
        return self.__state.sqlRecoveryPoint

    def increment_nonce(self):
        if self.__state is None:
            return 0
        else:
            self.__state.nonce += 1
            return self.__state.nonce

    @staticmethod
    def generate_address(pubkey):
        pubkey_x = pubkey.point.x()
        x_bytes = int_to_string(pubkey_x)
        pubkey_y = pubkey.point.y()
        head = bytes([2] if 0 == pubkey_y % 2 else [3])
        return head + x_bytes

    @staticmethod
    def encode_address(address):
        v = Account.ADDRESS_VERSION + address
        return base58.b58encode_check(v).decode('utf-8')

    @staticmethod
    def decode_address(address):
        v = base58.b58decode_check(address)
        return v[len(Account.ADDRESS_VERSION):]

    @staticmethod
    def encode_private_key(private_key):
        v = Account.PRIVATE_KEY_VERSION + private_key
        return base58.b58encode_check(v).decode('utf-8')

    @staticmethod
    def decode_private_key(private_key):
        v = base58.b58decode_check(private_key)
        return v[len(Account.PRIVATE_KEY_VERSION):]

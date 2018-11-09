# -*- coding: utf-8 -*-

import ecdsa
import hashlib
import base58

from ecdsa.ecdsa import int_to_string
from ecdsa.util import number_to_string, string_to_number
from google.protobuf.json_format import MessageToJson

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


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

        if password is None:
            # TODO raise exception
            assert 1 == 0

        if isinstance(password, bytes):
            password = password.decode('utf-8')
        self.password = password

        if private_key is None:
            self.__generate_new_key()
        else:
            self.__get_key(private_key)

        self.__state = None

    @staticmethod
    def _canonicalize_int(n, order):
        b = number_to_string(n, order)
        if (b[0] & 80) != 0:
            b = bytes([0]) + b
        return b

    def _serialize(self, r, s):
        order = self.__private_key.public_key.generator.order()
        half_order = order >> 1
        if s > half_order:
            s = order - s

        rb = self._canonicalize_int(r, order)
        sb = self._canonicalize_int(s, order)

        length = 4 + len(rb) + len(sb)
        b = b'\x30' + bytes([length])
        b += b'\x02' + bytes([len(rb)]) + rb
        b += b'\x02' + bytes([len(sb)]) + sb
        return b

    @staticmethod
    def _deserialize(sig):
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

    def sign_msg_hash(self, msg_hash):
        r, s = self.__signing_key.sign_number(string_to_number(msg_hash))
        return self._serialize(r, s)

    def verify_sign(self, msg_hash, sign):
        r, s = self._deserialize(sign)
        signature = ecdsa.ecdsa.Signature(r, s)
        return self.__private_key.public_key.verifies(string_to_number(msg_hash), signature)

    def __generate_new_key(self):
        self.__signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                                       hashfunc=hashlib.sha256)
        self.__private_key = self.__signing_key.privkey
        self.__address = Account.generate_address(self.__private_key.public_key)

    def __get_key(self, private_key):
        if isinstance(private_key, str):
            private_key = Account.decode_private_key(private_key)

        d = int.from_bytes(private_key, byteorder='big')
        sk = ecdsa.SigningKey.from_secret_exponent(secexp=d,
                                                   curve=ecdsa.SECP256k1,
                                                   hashfunc=hashlib.sha256)
        self.__signing_key = sk
        self.__private_key = self.__signing_key.privkey
        self.__address = Account.generate_address(self.__private_key.public_key)

    def __get_private_key_bytes(self):
        d = self.__private_key.secret_multiplier
        return d.to_bytes(Account.PRIVATE_KEY_BYTES_LENGTH, byteorder='big')

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

    @nonce.setter
    def nonce(self, v):
        if self.__state.nonce >= v:
            return
        self.__state.nonce = v

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

    @staticmethod
    def encrypt_account(account):
        """
        https://cryptography.io/en/latest/hazmat/primitives/aead/
        :param account: account to export
        :return: encrypted account data (bytes)
        """
        password = account.password.encode('utf-8')

        m = hashlib.sha256()
        m.update(password)
        hash_pw = m.digest()

        m = hashlib.sha256()
        m.update(password)
        m.update(hash_pw)
        enc_key = m.digest()

        nonce = hash_pw[4:16]
        aesgcm = AESGCM(enc_key)
        return aesgcm.encrypt(nonce=nonce,
                              data=account.private_key,
                              associated_data=b'')

    @staticmethod
    def decrypt_account(encrypted_bytes, password):
        """
        https://cryptography.io/en/latest/hazmat/primitives/aead/
        :param encrypted_bytes: encrypted data (bytes) of account
        :param password: to decrypt the exported bytes
        :return: account instance
        """
        if isinstance(password, str):
            password = password.encode('utf-8')

        m = hashlib.sha256()
        m.update(password)
        hash_pw = m.digest()

        m = hashlib.sha256()
        m.update(password)
        m.update(hash_pw)
        dec_key = m.digest()

        nonce = hash_pw[4:16]
        aesgcm = AESGCM(dec_key)
        dec_value = aesgcm.decrypt(nonce=nonce,
                                   data=encrypted_bytes,
                                   associated_data=b'')

        return Account(password=password, private_key=dec_value)

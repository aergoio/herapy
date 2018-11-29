# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .obj import private_key as pk
from .obj import address as addr

from .utils.encoding import decode_address


class Account:
    def __init__(self, password, private_key=None, empty=False):
        if empty:
            self.__private_key = None
            self.__address = None
            self.__state = None
            self.__state_proof = None
            return

        if password is None:
            # TODO raise exception
            assert 1 == 0

        if isinstance(password, bytes):
            password = password.decode('utf-8')
        self.password = password

        self.__private_key = pk.PrivateKey(private_key)
        self.__address = addr.Address(self.__private_key.public_key)
        self.__state = None
        self.__state_proof = None

    def sign_msg_hash(self, msg_hash):
        return self.__private_key.sign_msg(msg_hash)

    def verify_sign(self, msg_hash, sign):
        return self.__private_key.verify_sign(msg_hash, sign)

    @property
    def private_key(self):
        return self.__private_key

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
            v = decode_address(v)
        self.__address = v

    @property
    def state(self):
        if self.__state is None:
            return None
        return MessageToJson(self.__state)

    @state.setter
    def state(self, v):
        self.__state = v

    @property
    def state_proof(self):
        if self.__state_proof is None:
            return None
        return MessageToJson(self.__state_proof)

    @state_proof.setter
    def state_proof(self, v):
        self.__state_proof = v

    @property
    def nonce(self):
        if self.__state is None:
            return -1
        return self.__state.nonce

    @nonce.setter
    def nonce(self, v):
        if self.__state.nonce >= v:
            return
        self.__state.nonce = v

    @property
    def balance(self):
        if self.__state is None:
            return -1
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
                              data=bytes(account.private_key),
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

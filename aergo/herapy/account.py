# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .obj import address as addr
from .obj import aer
from .obj import private_key as pk

from .utils.encoding import decode_address, decode_root
from .utils import merkle_proof as mp


class Account:
    """ Account can be a user account with private and public key,
    or a contract account.
    """
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

    def __str__(self):
        if self.__state_proof:
            return MessageToJson(self.__state_proof)
        elif self.__state:
            return self.state
        return super().__str__()

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
        return self.__state_proof

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
            return aer.Aer()
        return aer.Aer(int.from_bytes(self.__state.balance, 'big'))

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

    def verify_inclusion(self, root):
        """ verify_inclusion verifies the contract state is included in the
        general trie root.
        """
        if self.__state_proof is None:
            return False
        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)
        key = hashlib.sha256(self.__address).digest()
        value = hashlib.sha256(self.__state.SerializeToString()).digest()
        ap = self.__state_proof.auditPath
        if self.__state_proof.bitmap:
            height = self.__state_proof.height
            bitmap = self.__state_proof.bitmap
            return mp.verify_inclusion_c(ap, height, bitmap, root, key, value)
        return mp.verify_inclusion(ap, root, key, value)

    def verify_exclusion(self, root):
        """ verify_exclusion verifies that the contract state doesnt exist
        in the general trie root.
        """
        if self.__state_proof is None:
            return False
        key = hashlib.sha256(self.__address).digest()
        if self.__state_proof.bitmap:
            return mp.verify_exclusion_c(root,
                                         self.__state_proof.auditPath,
                                         self.__state_proof.height,
                                         self.__state_proof.bitmap,
                                         key,
                                         self.__state_proof.proofKey,
                                         self.__state_proof.proofVal)
        return mp.verify_exclusion(root,
                                   self.__state_proof.auditPath,
                                   key,
                                   self.__state_proof.proofKey,
                                   self.__state_proof.proofVal)

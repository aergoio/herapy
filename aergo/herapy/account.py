# -*- coding: utf-8 -*-

import hashlib
import json

from google.protobuf.json_format import MessageToJson
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .obj import address as addr
from .obj import aer
from .obj import private_key as pk

from .utils.encoding import decode_address, decode_root
from .utils import merkle_proof as mp
from .utils.converter import encrypt_bytes, decrypt_bytes

from .errors.general_exception import GeneralException


class Account:
    """ Account can be a user account with private and public key,
    or a contract account.
    """
    def __init__(self, private_key=None, empty=False):
        if empty:
            self.__private_key = None
            self.__address = None
            self.__state = None
            self.__state_proof = None
            return

        self.__private_key = pk.PrivateKey(private_key)
        self.__address = self.__private_key.address
        self.__state = None
        self.__state_proof = None

    def __str__(self):
        state = self.state
        if self.__state_proof:
            state = MessageToJson(self.__state_proof)

        if state:
            state = json.loads(state)

        account = {
            "address": str(self.__address),
            "balance": str(self.balance),
            "nonce": str(self.nonce),
            "state": state,
        }
        return json.dumps(account, indent=2)

    def sign_msg_hash(self, msg_hash):
        return self.__private_key.sign_msg(msg_hash)

    def verify_sign(self, msg_hash, sign):
        return self.__private_key.verify_sign(msg_hash, sign)

    @property
    def private_key(self):
        return self.__private_key

    @property
    def public_key(self):
        if self.__private_key is not None:
            return self.__private_key.public_key

        if self.__address is not None:
            return self.__address.public_key

        return None

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, v):
        if self.__address is not None:
            raise ValueError('not empty account')

        self.__address = addr.Address(None, empty=True)
        self.__address.value = v

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
        if self.__state.nonce > v:
            raise ValueError("the nonce value should be bigger than the current nonce value: {}".format(self.__state.nonce))
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
    def encrypt_account(account, password):
        """
        https://cryptography.io/en/latest/hazmat/primitives/aead/
        :param account: account to export
        :return: encrypted account data (bytes)
        """
        return encrypt_bytes(bytes(account.private_key), password)

    @staticmethod
    def decrypt_account(encrypted_bytes, password):
        """
        https://cryptography.io/en/latest/hazmat/primitives/aead/
        :param encrypted_bytes: encrypted data (bytes) of account
        :param password: to decrypt the exported bytes
        :return: account instance
        """
        try:
            dec_value = decrypt_bytes(encrypted_bytes, password)
        except InvalidTag as e:
            raise GeneralException("Fail to decrypt an account. Please check the password.") from e
        return Account(private_key=dec_value)

    def verify_proof(self, root):
        """ verify that the given inclusion and exclusion proofs are correct """
        if self.__state_proof is None:
            return False

        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)

        if bytes(self.__address) != self.__state_proof.key:
            return False

        trie_key = hashlib.sha256(self.__state_proof.key).digest()
        value = hashlib.sha256(self.__state_proof.state.SerializeToString()).digest()
        ap = self.__state_proof.auditPath

        if self.__state_proof.bitmap:
            height = self.__state_proof.height
            bitmap = self.__state_proof.bitmap
            if self.__state_proof.inclusion:
                return mp.verify_inclusion_c(ap, height, bitmap, root, trie_key, value)
            else:
                return mp.verify_exclusion_c(root, ap, height, bitmap, trie_key,
                                             self.__state_proof.proofKey,
                                             self.__state_proof.proofVal)
        else:
            if self.__state_proof.inclusion:
                return mp.verify_inclusion(ap, root, trie_key, value)
            else:
                return mp.verify_exclusion(root, ap, trie_key,
                                           self.__state_proof.proofKey,
                                           self.__state_proof.proofVal)

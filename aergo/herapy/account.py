# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .obj import private_key as pk
from .obj import address as addr

from .utils.encoding import decode_address, decode_root
from .utils.byte_tools import bit_is_set


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

    def verify_inclusion(self, root):
        if self.__state_proof is None:
            return False
        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)
        key = hashlib.sha256(self.__address).digest()
        value = hashlib.sha256(self.__state.SerializeToString()).digest()
        if self.__state_proof.bitmap:
            return self._verify_inclusion_c(root, key, value)
        return self._verify_inclusion(root, key, value)

    def _verify_inclusion(self, root, key, value):
        leaf_hash = hashlib.sha256(key + value +
                                    bytes([256-len(self.__state_proof.auditPath)])).digest()
        return root == self._verify_proof(self.__state_proof.auditPath, 0, key, leaf_hash)

    def _verify_inclusion_c(self, root, key, value):
        leaf_hash = hashlib.sha256(key + value +
                                    bytes([256-self.__state_proof.height])).digest()
        return root == self._verify_proof_c(self.__state_proof.bitmap, key, leaf_hash,
                                            self.__state_proof.auditPath,
                                            self.__state_proof.height, 0, 0)

    def _verify_proof(self, ap, key_index, key, leaf_hash):
        if key_index == len(ap):
            return leaf_hash
        if bit_is_set(key, key_index):
            return hashlib.sha256(ap[len(ap)-key_index-1] +
                                  self._verify_proof(ap, key_index+1, key, leaf_hash)).digest()
        return hashlib.sha256(self._verify_proof(ap, key_index+1, key, leaf_hash) +
                              ap[len(ap)-key_index-1]).digest()

    def _verify_proof_c(self, bitmap, key, leaf_hash, ap, length, key_index, ap_index):
        if key_index == length:
            return leaf_hash
        if bit_is_set(key, key_index):
            if bit_is_set(bitmap, length-key_index-1):
                return hashlib.sha256(ap[len(ap)-ap_index-1] +
                                      self._verify_proof_c(bitmap, key, leaf_hash, ap, length,
                                                          key_index+1, ap_index+1)).digest()
            return hashlib.sha256(bytes([0]) +
                                  self._verify_proof_c(bitmap, key, leaf_hash, ap, length,
                                                      key_index+1, ap_index)).digest()
        if bit_is_set(bitmap, length-key_index-1):
            return hashlib.sha256(self._verify_proof_c(bitmap, key, leaf_hash, ap, length,
                                                      key_index+1, ap_index+1) +
                                  ap[len(ap)-ap_index-1]).digest()
        return hashlib.sha256(self._verify_proof_c(bitmap, key, leaf_hash, ap, length,
                                                  key_index+1, ap_index) +
                              bytes([0])).digest()

    def verify_exclusion(self, root):
        if self.__state_proof is None:
            return False
        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)
        key = hashlib.sha256(self.__address).digest()
        bitmap = self.__state_proof.bitmap
        auditPath = self.__state_proof.auditPath
        length = self.__state_proof.height
        proofKey = self.__state_proof.proofKey
        proofVal = self.__state_proof.proofVal

        if not proofKey:
            # return true if a DefaultLeaf in the key path is included in the trie
            if bitmap:
                return root == self._verify_proof_c(bitmap, key, bytes([0]), auditPath,
                                                    length, 0, 0)
            else:
                return root == self._verify_proof(auditPath, 0, key, bytes([0]))
            # return bytes.Equal(s.Root, s.verifyInclusion(ap, 0, key, DefaultLeaf))
        # Check if another kv leaf is on the key path in 2 steps
        # 1- Check the proof leaf exists
        if bitmap:
            if not self._verify_inclusion_c(root, proofKey, proofVal):
                # the proof leaf is not included in the trie
                return False
        else:
            if not self._verify_inclusion(root, proofKey, proofVal):
                # the proof leaf is not included in the trie
                return False

        # 2- Check the proof leaf is on the key path
        for b in range(len(auditPath)):
            if bit_is_set(key, b) != bit_is_set(proofKey, b):
                # the proofKey leaf node is not on the path of the key
                return False
        # return true because we verified another leaf is on the key path
        return True

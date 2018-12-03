# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from aergo.herapy.utils import merkle_proof as mp


class VarProof:
    def __init__(self, var_proof, var_name, var_index=""):
        self.__var_proof = var_proof
        self.__var_name = var_name
        self.__var_index = var_index
        var_id = bytes("_" + var_name + var_index, "utf-8")
        self.__trie_key = hashlib.sha256(var_id).digest()

    @property
    def var_index(self):
        return self.__var_index

    @property
    def var_name(self):
        return self.__var_name

    @property
    def trie_key(self):
        return self.__trie_key

    @property
    def var_proof(self):
        return MessageToJson(self.__var_proof)

    @var_proof.setter
    def var_proof(self, v):
        self.__var_proof = v

    def verify_inclusion(self, root):
        if self.__var_proof is None:
            return False
        key = self.__trie_key
        value = hashlib.sha256(self.__var_proof.value).digest()
        ap = self.__var_proof.auditPath
        if self.__var_proof.bitmap:
            height = self.__var_proof.height
            bitmap = self.__var_proof.bitmap
            return mp.verify_inclusion_c(ap, height, bitmap, root, key, value)
        return mp.verify_inclusion(ap, root, key, value)

    def verify_exclusion(self, root):
        if self.__var_proof is None:
            return False
        if self.__var_proof.bitmap:
            return mp.verify_exclusion_c(root,
                                         self.__var_proof.auditPath,
                                         self.__var_proof.height,
                                         self.__var_proof.bitmap,
                                         self.__trie_key,
                                         self.__var_proof.proofKey,
                                         self.__var_proof.proofVal)
        return mp.verify_exclusion(root,
                                   self.__var_proof.auditPath,
                                   self.__trie_key,
                                   self.__var_proof.proofKey,
                                   self.__var_proof.proofVal)

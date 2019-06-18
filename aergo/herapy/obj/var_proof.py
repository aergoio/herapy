# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from aergo.herapy.utils import merkle_proof as mp


class VarProofs(list):
    """ VarProof holds the inclusion/exclusion proof of a variable state
    inside a contract state trie
    """
    def __init__(self, var_proofs, storage_keys):
        self.__var_proofs = var_proofs
        self.__storage_keys = storage_keys
        list.__init__(self, var_proofs[:])

    def __str__(self):
        json_string = ""
        for proof in self.__var_proofs:
            json_string += MessageToJson(proof)
        return json_string

    @property
    def var_proofs(self):
        return self.__var_proofs

    @property
    def storage_keys(self):
        return self.__storage_keys

    def verify_var_proof(self, root, var_proof, trie_key):
        if var_proof.key != trie_key:
            return False
        value = hashlib.sha256(var_proof.value).digest()
        ap = var_proof.auditPath

        if var_proof.bitmap:
            height = var_proof.height
            bitmap = var_proof.bitmap

            if var_proof.inclusion:
                return mp.verify_inclusion_c(ap, height, bitmap, root, trie_key, value)
            else:
                return mp.verify_exclusion_c(root, ap, height, bitmap, trie_key,
                                             var_proof.proofKey,
                                             var_proof.proofVal)
        else:
            if var_proof.inclusion:
                return mp.verify_inclusion(ap, root, trie_key, value)
            else:
                return mp.verify_exclusion(root, ap, trie_key,
                                           var_proof.proofKey,
                                           var_proof.proofVal)

    def verify_proof(self, root):
        """verify that the given inclusion and exclusion proofs are correct """
        if self.__var_proofs is None or 0 == self.__len__():
            return False

        for i, storage_proof in enumerate(self.__var_proofs):
            if not self.verify_var_proof(root, storage_proof, self.storage_keys[i]):
                return False
        return True

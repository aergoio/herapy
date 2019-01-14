# -*- coding: utf-8 -*-

import hashlib

from google.protobuf.json_format import MessageToJson
from aergo.herapy.utils import merkle_proof as mp


class VarProofs:
    """ VarProof holds the inclusion/exclusion proof of a variable state
    inside a contract state trie
    """
    def __init__(self, var_proofs):
        self.__var_proofs = var_proofs

    def __str__(self):
        json_string = ""
        for proof in self.__var_proofs:
            json_string += MessageToJson(proof)
        return json_string

    @property
    def var_proofs(self):
        return self.__var_proofs

    def verify_proof(self, root):
        """ verify that the given inclusion and exclusion proofs are correct """
        if self.__var_proofs is None:
            return False
        for storage_proof in self.__var_proofs:
            var_id = bytes(storage_proof.key, 'utf-8')
            trie_key = hashlib.sha256(var_id).digest()
            value = hashlib.sha256(storage_proof.value).digest()
            ap = storage_proof.auditPath
            if storage_proof.bitmap:
                height = storage_proof.height
                bitmap = storage_proof.bitmap
                if storage_proof.inclusion:
                    if not mp.verify_inclusion_c(ap, height, bitmap, root, trie_key, value):
                        return False
                else:
                    if not mp.verify_exclusion_c(root, ap, height, bitmap, trie_key,
                                                 storage_proof.proofKey,
                                                 storage_proof.proofVal):
                        return False
            else:
                if storage_proof.inclusion:
                    if not mp.verify_inclusion(ap, root, trie_key, value):
                        return False
                else:
                    if not mp.verify_exclusion(root, ap, trie_key,
                                               storage_proof.proofKey,
                                               storage_proof.proofVal):
                        return False
        return True

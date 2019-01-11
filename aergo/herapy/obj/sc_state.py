# -*- coding: utf-8 -*-

from google.protobuf.json_format import MessageToJson


class SCState:
    """ SCState holds the inclusion/exclusion proofs of a contract
    state in the global trie and of a variable's value in the
    contract trie.
    SCState is returned by aergo.query_sc_state() for easy merkle
    proof verification give a root.
    """
    def __init__(self, account, var_proofs):
        self.__account = account
        self.__var_proofs = var_proofs

    def __str__(self):
        account_str = MessageToJson(self.__account.state_proof)
        var_str = str(self.__var_proofs)
        return account_str + var_str

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, v):
        self.__account = v

    @property
    def var_proof(self):
        return self.__var_proofs

    @var_proof.setter
    def var_proof(self, v):
        self.__var_proofs = v

    def verify_proof(self, root):
        """ verify that the given inclusion and exclusion proofs are correct """
        if not self.__account.verify_proof(root):
            return False
        sc_root = self.__account.state_proof.state.storageRoot
        if not self.__var_proofs.verify_proof(sc_root):
            return False
        return True


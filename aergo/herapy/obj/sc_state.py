# -*- coding: utf-8 -*-

from google.protobuf.json_format import MessageToJson


class SCState:
    """ SCState holds the inclusion/exclusion proofs of a contract
    state in the global trie and of a variable's value in the
    contract trie.
    SCState is returned by aergo.query_sc_state() for easy merkle
    proof verification give a root.
    """
    def __init__(self, account, var_proof):
        self.__account = account
        self.__var_proof = var_proof

    def __str__(self):
        account_str = MessageToJson(self.__account.state_proof)
        var_str = str(self.__var_proof)
        return account_str + var_str

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, v):
        self.__account = v

    @property
    def var_proof(self):
        return self.__var_proof

    @var_proof.setter
    def var_proof(self, v):
        self.__var_proof = v

    def verify_inclusion(self, root):
        """ verify_inclusion verifies the contract state is included in the
        general trie root and the variable state is included in that contract
        state.
        """
        if not self.__account.verify_inclusion(root):
            # The contract state doesnt exist
            return False
        sc_root = self.__account.state_proof.state.storageRoot
        # Verify the variable state is included in the contract root
        return self.__var_proof.verify_inclusion(sc_root)

    def verify_exclusion(self, root):
        """ verify_exclusion verifies that the contract state doesnt exist,
        if it does then verify the variable is not included in that
        contract state.
        """
        if self.__account.verify_exclusion(root):
            # The contract state doesnt exist
            return True
        # First verify that the contract state does exist before proving
        # that the variable state doesnt exist
        if not self.__account.verify_inclusion(root):
            # The contract state doesnt exist so the variable exclusion proof
            # cannot be valid
            return False
        sc_root = self.__account.state_proof.state.storageRoot
        return self.__var_proof.verify_exclusion(sc_root)

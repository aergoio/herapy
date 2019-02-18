# -*- coding: utf-8 -*-

from google.protobuf.json_format import MessageToJson


class SCStateVar:
    """
    SCStateVar represents each variable of a calling smart contract.
    If the variable is the 'state.var' type,
    you can skip 'array_index' and 'map_key'.
    If the variable is the 'state.array' type,
    use 'array_index' with the index number.
    If the variable is the 'state.map' type,
    use 'map_key' with the key name of the map.
    """
    def __init__(self, var_name, array_index=None, map_key=None, empty=False):
        if empty:
            return

        self.var_name = var_name
        self.array_indx = array_index
        self.map_key = map_key

        self.get_storage_key()

    def get_storage_key(self):
        if self.array_indx is not None:
            self.storage_key = '_sv_{0}-{1}'.format(self.var_name, self.array_indx)
        elif self.map_key is not None:
            self.storage_key = '_sv_{0}-{1}'.format(self.var_name, self.map_key)
        else:
            self.storage_key = '_sv_{0}'.format(self.var_name)

    def __str__(self):
        return self.storage_key


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

    @property
    def var_proofs(self):
        return self.__var_proofs

    @var_proofs.setter
    def var_proofs(self, v):
        self.__var_proofs = v

    def verify_proof(self, root):
        """ verify that the given inclusion and exclusion proofs are correct """
        if not self.__account.verify_proof(root):
            return False

        sc_root = self.__account.state_proof.state.storageRoot
        return self.__var_proofs.verify_proof(sc_root)


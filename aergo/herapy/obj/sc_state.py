# -*- coding: utf-8 -*-


class SCState:
    def __init__(self, account, var_proof):
        self.__account = account
        self.__var_proof = var_proof

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
        if not self.__account.verify_inclusion(root):
            return False
        sc_root = self.__account.state_proof.state.storageRoot
        return self.__var_proof.verify_inclusion(sc_root)

    def verify_exclusion(self, root):
        if self.__account.verify_exclusion(root):
            return True
        if not self.__account.verify_inclusion(root):
            return False
        sc_root = self.__account.state_proof.state.storageRoot
        return self.__var_proof.verify_exclusion(sc_root)


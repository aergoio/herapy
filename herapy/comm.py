# -*- coding: utf-8 -*-

import grpc

from herapy.grpc import account_pb2, rpc_pb2, rpc_pb2_grpc


class Comm:
    def __init__(self, target=None):
        self.__channel = None
        self.__rpc_stub = None

        if target is not None:
            self.connect(target)

    def connect(self, target):
        self.disconnect()

        self.__channel = grpc.insecure_channel(target)
        self.__rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(self.__channel)

    def disconnect(self):
        if self.__channel is not None:
            self.__channel.close()

    def get_account_state(self, address):
        if self.__rpc_stub is None:
            return None

        rpc_account = account_pb2.Account()
        rpc_account.address = address
        return self.__rpc_stub.GetState(rpc_account)

    def get_blockchain_status(self):
        if self.__rpc_stub is None:
            return None

        return self.__rpc_stub.Blockchain(rpc_pb2.Empty())

    # TODO unnecessary functions
    '''
    def get_accounts(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.GetAccounts(rpc_pb2.Empty())

    def unlock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        personal.account.address = address
        return self.__rpc_stub.UnlockAccount(personal)

    def lock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.account.address = address
        personal.passphrase = passphrase
        return self.__rpc_stub.LockAccount(personal)
    '''

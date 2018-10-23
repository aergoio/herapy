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

    def get_account_state(self, account):
        if self.__rpc_stub is None:
            return None

        rpc_account = account_pb2.Account()
        rpc_account.address = account.address
        return self.__rpc_stub.GetState(rpc_account)

    def get_accounts(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.GetAccounts(rpc_pb2.Empty())

    def get_tx(self, tx_hash):
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        return self.__rpc_stub.GetTX(single_bytes)

    def send_tx(self, tx):
        return self.__rpc_stub.SendTX(tx)

    def commit_tx(self, tx):
        return self.__rpc_stub.CommitTX(tx)

    def get_peers(self):
        return self.__rpc_stub.GetPeers(rpc_pb2.Empty())

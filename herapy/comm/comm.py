# -*- coding: utf-8 -*-

import grpc
import base58

from google.protobuf.json_format import MessageToJson

from herapy.grpc import rpc_pb2
from herapy.grpc import rpc_pb2_grpc
from herapy.grpc import account_pb2

class Comm:
    def __init__(self, target):
        self.channel = grpc.insecure_channel(target)
        self.rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(self.channel)
        self.result = b''

    def get_result_to_json(self):
        return MessageToJson(self.result)

    def get_blockchain_status(self):
        self.result = self.rpc_stub.Blockchain(rpc_pb2.Empty())
        return self.result

    def create_account(self, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        self.result = self.rpc_stub.CreateAccount(personal)
        return self.result

    def get_account_state(self, account):
        self.result = self.rpc_stub.GetState(account)
        return self.result

    def get_account_state_from_address(self, address):
        account = account_pb2.Account()
        account.address = address
        return self.get_account_state(account)

    def get_account_state_from_b58address(self, b58address):
        return self.get_account_state_from_address(base58.b58decode_check(b58address))

    # return locked account
    def lock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.account.address = address
        personal.passphrase = passphrase
        self.result = self.rpc_stub.LockAccount(personal)
        return self.result

    # return locked account
    def lock_account_from_b58address(self, b58address, passphrase):
        return self.lock_account(base58.b58decode_check(b58address), passphrase)

    # return unlocked account
    def unlock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        personal.account.address = address
        self.result = self.rpc_stub.UnlockAccount(personal)
        return self.result

    # return unlocked account
    def unlock_account_from_b58address(self, b58address, passphrase):
        return self.unlock_account(base58.b58decode_check(b58address), passphrase)

    # return account list
    def get_accounts(self):
        self.result = self.rpc_stub.GetAccounts(rpc_pb2.Empty())
        return self.result


# -*- coding: utf-8 -*-

import grpc
import hashlib

from google.protobuf.json_format import MessageToJson

from herapy.grpc import rpc_pb2
from herapy.grpc import rpc_pb2_grpc


def calculate_tx_hash(tx):
    m = hashlib.sha256()
    tx_bytes = tx.body.nonce.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.account)
    m.update(tx.body.recipient)
    tx_bytes = tx.body.amount.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.payload)
    tx_bytes = tx.body.limit.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    tx_bytes = tx.body.price.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    tx_bytes = tx.body.type.to_bytes(4, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.sign)
    return m.digest()


class Comm:
    def __init__(self, target):
        self.channel = grpc.insecure_channel(target)
        self.rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(self.channel)
        self.result = None

    def get_result_to_json(self):
        return MessageToJson(self.result)

    # XXX works not well. what for?
    def get_node_state(self, timeout):
        timeout_b = timeout.to_bytes(8, byteorder='little')
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = timeout_b
        self.result = self.rpc_stub.NodeState(single_bytes)
        return self.result

    def get_blockchain_status(self):
        self.result = self.rpc_stub.Blockchain(rpc_pb2.Empty())
        return self.result

    def get_block_headers(self, block_hash=b'', height=0, size=20, offset=0, order_by_asc=True):
        params = rpc_pb2.ListParams()
        params.hash = block_hash
        params.height = height
        params.size = size
        params.offset = offset
        params.asc = order_by_asc
        self.result = self.rpc_stub.ListBlockHeaders(params)
        return self.result

    def get_block(self, block_hash=None, block_height=0):
        single_bytes = rpc_pb2.SingleBytes()

        if block_hash is None:
            block_height_b = block_height.to_bytes(8, byteorder='little')
            single_bytes.value = block_height_b
        else:
            single_bytes.value = block_hash

        self.result = self.rpc_stub.GetBlock(single_bytes)
        return self.result

    def get_tx(self, tx_hash):
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        self.result = self.rpc_stub.GetTX(single_bytes)
        return self.result

    def get_block_tx(self, tx_hash):
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        self.result = self.rpc_stub.GetTX(single_bytes)
        return self.result

    def get_receipt(self):
        pass

    def get_abi(self):
        pass

    def send_tx(self, tx, key_manager, nonce=-1):
        if nonce == -1:
            # TODO find the last nonce value
            raise NotImplementedError('nonce should be set.')
        else:
            tx.body.nonce = nonce

        # sign transaction
        tx.body.sign = key_manager.sign_message(tx)

        tx.hash = calculate_tx_hash(tx)
        self.result = self.rpc_stub.SendTX(tx)

    def get_state(self):
        pass

    def get_account_state(self, account):
        self.result = self.rpc_stub.GetState(account)
        return self.result

    # return account list
    def get_accounts(self):
        self.result = self.rpc_stub.GetAccounts(rpc_pb2.Empty())
        return self.result

    def verify_tx(self):
        pass

    def query_contract(self):
        pass

    def get_peers(self):
        self.result = self.rpc_stub.GetPeers(rpc_pb2.Empty())
        return self.result

    def get_votes(self):
        pass

    """
    ############################################
    # functions which don't need for a client library
    ###########
    def sign_tx(self):
        pass

    def create_account(self, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase

    # XXX why???
    # return locked account
    def lock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.account.address = address
        personal.passphrase = passphrase
        self.result = self.rpc_stub.LockAccount(personal)
        return self.result

    # XXX why???
    # return unlocked account
    def unlock_account(self, address, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        personal.account.address = address
        self.result = self.rpc_stub.UnlockAccount(personal)
        return self.result

    def commit_tx(self):
        pass
    """


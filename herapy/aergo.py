# -*- coding: utf-8 -*-

"""Main module."""

import json

from google.protobuf.json_format import MessageToJson

from . import account as acc
from . import comm
from . import block
from . import transaction
from .peer import Peer
from .grpc import blockchain_pb2

class Aergo:
    def __init__(self):
        self.__account = None
        self.__comm = None

    @property
    def account(self):
        """
        Returns the account object.
        :return:
        """
        return self.__account

    def create_account(self, password):
        """
        Creates a new account with password `password`.
        :param password:
        :return:
        """
        self.__account = acc.Account(password)
        return self.__comm.create_account(address=self.__account.address, passphrase=password)

    def new_account(self, password=None, private_key=None):
        self.__account = acc.Account(password, private_key)
        if private_key is not None:
            self.get_account_state()
        return self.__account

    def get_account_state(self, account=None):
        """
        Return the account state of account `account`.
        :param account:
        :return:
        """
        if self.__comm is None:
            return None

        if account is None:
            address = self.__account.address
        else:
            address = account.address

        state = self.__comm.get_account_state(address)

        if account is None:
            self.__account.state = state
        else:
            account.state = state

        return MessageToJson(state)

    def connect(self, target):
        """
        Connect to the gRPC server running on port `target` e.g. target="localhost:7845".
        :param target:
        :return:
        """
        if target is None:
            raise ValueError('need target value')

        self.__comm = comm.Comm(target)
        self.__comm.connect()

    def disconnect(self):
        """
        Disconnect from the gRPC server.
        """
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_blockchain_status(self):
        """
        Returns the highest block hash and block height so far.
        :return:
        """
        if self.__comm is None:
            return None, -1

        status = self.__comm.get_blockchain_status()
        return status.best_block_hash, status.best_height

    def get_block(self, block_hash=None, block_height=-1):
        """
        Returns information about block `block_hash`.
        :param block_hash:
        :param block_height:
        :return:
        """
        if self.__comm is None:
            return None

        if block_height > 0:
            query = block_height.to_bytes(8, byteorder='little')
        else:
            if isinstance(block_hash, str):
                block_hash = block.Block.decode_block_hash(block_hash)

            query = block_hash

        result = self.__comm.get_block(query)
        b = block.Block()
        b.info = result
        return b

    def get_node_accounts(self):
        """
        Returns a list of all node accounts.
        :return:
        """
        result = self.__comm.get_accounts()
        accounts = []
        for a in result.accounts:
            account = acc.Account("", empty=True)
            account.address = a.address
            accounts.append(account)

        return accounts

    def get_peers(self):
        """
        Returns a list of peers.
        :return:
        """
        result = self.__comm.get_peers()
        peers = []
        for i in range(len(result.peers)):
            p = result.peers[i]
            s = result.states[i]
            peer = Peer()
            peer.info = p
            peer.state = s
            peers.append(peer)

        return peers

    def get_node_state(self, timeout=1):
        """
        Returns information about the node state.
        :return:
        """
        result = self.__comm.get_node_state(timeout)
        json_txt = result.value.decode('utf8').replace("'", '"')
        return json.loads(json_txt)

    def get_tx(self, tx_hash):
        """
        Returns info on transaction with hash `tx_hash`.
        :param tx_hash:
        :return:
        """
        return self.__comm.get_tx(tx_hash)

    def lock_account(self, address, passphrase):
        """
        Locks the account with address `address` with the passphrase `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        return self.__comm.lock_account(address, passphrase)

    def unlock_account(self, address, passphrase):
        """
        Unlocks the account with address `address` with the passphrase `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        return self.__comm.unlock_account(address=address, passphrase=passphrase)

    def send_payload(self, to_address, amount, payload):
        if self.__comm is None:
            return None, None

        tx = transaction.Transaction(from_address=self.__account.address,
                                     to_address=to_address,
                                     nonce=self.__account.nonce,
                                     amount=amount,
                                     payload=payload)
        tx.sign = self.__account.sign_message(tx.calculate_hash())
        return tx, self.__comm.send_tx(tx)

    def send_tx(self, signed_tx):
        """
        Sends the transaction `tx`.
        :param signed_tx:
        :return:
        """
        ""
        return self.__comm.send_tx(signed_tx)

    def commit_tx(self, signed_txs):
        """
        Send a set of transactions `txs` simultaneously.
        :param signed_txs:
        :return:
        """
        return self.__comm.commit_tx(signed_txs)

    def import_account(self, exported_data, password):
        if isinstance(exported_data, str):
            exported_data = acc.Account.decode_private_key(exported_data)

        if isinstance(password, str):
            password = password.encode('utf-8')

        return acc.Account.decrypt_account(exported_data, password)

    def export_account(self, account=None):
        if account is None:
            account = self.__account

        enc_acc = acc.Account.encrypt_account(account)
        return acc.Account.encode_private_key(enc_acc)

"""
    def call_sc(self, sc_address, func_name, args):
        caller = self.__account
        if caller.state is None:
            self.get_account_state(caller)

        nonce = caller.nonce + 1

        sc_account = acc.Account(password=None, empty=True)
        sc_account.address = sc_address

        call_info = {
            'Name': func_name,
            'Args': args
        }
        payload = str(json.dumps(call_info)).encode('utf-8')

        tx = transaction.Transaction(from_address=caller.address,
                                     to_address=sc_account.address,
                                     nonce=nonce,
                                     payload=payload)
        tx.sign = caller.sign_message(tx.calculate_hash())
        commit_result = self.commit_tx([tx])
        return commit_result[0]

    def query_sc(self, sc_address, func_name, args):
        sc_account = acc.Account(password=None, empty=True)
        sc_account.address = sc_address

        call_info = {
            'Name': func_name,
            'Args': args
        }
        payload = str(json.dumps(call_info)).encode('utf-8')

        tx = transaction.Transaction(from_address=caller.address,
                                     to_address=sc_account.address,
                                     nonce=nonce,
                                     payload=payload)
        tx.sign = caller.sign_message(tx.calculate_hash())
        commit_result = self.commit_tx([tx])
        return commit_result[0]
"""

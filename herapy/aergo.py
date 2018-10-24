# -*- coding: utf-8 -*-

"""Main module."""

import json

from google.protobuf.json_format import MessageToJson

from . import account as acc
from . import comm
from . import block
from .peer import Peer


class Aergo:
    def __init__(self):
        self.__account = None
        self.__comm = None

    @property
    def account(self):
        return self.__account

    def new_account(self, password, private_key=None):
        self.__account = acc.Account(password, private_key)
        if private_key is not None:
            self.get_account_state(self.__account.address)
        return self.__account

    def get_account_state(self, account=None):
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
        if target is None:
            raise ValueError('need target value')

        self.__comm = comm.Comm(target)
        self.__comm.connect()

    def disconnect(self):
        if self.__comm is not None:
            self.__comm.disconnect()

    def get_blockchain_status(self):
        if self.__comm is None:
            return None, -1

        status = self.__comm.get_blockchain_status()
        return status.best_block_hash, status.best_height

    def get_block(self, block_hash=None, block_height=-1):
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
        result = self.__comm.get_accounts()
        accounts = []
        for a in result.accounts:
            account = acc.Account("", empty=True)
            account.address = a.address
            accounts.append(account)

        return accounts

    def get_peers(self):
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
        result = self.__comm.get_node_state(timeout)
        json_txt = result.value.decode('utf8').replace("'", '"')
        return json.loads(json_txt)

    def get_tx(self, tx_hash):
        return self.__comm.get_tx(tx_hash)

    def commit_tx(self, tx):
        # sign transaction
        #tx.body.sign = self.__account.key_manager.sign_message(tx)
        #tx.hash = calculate_tx_hash(tx)
        #return self.__comm.commit_tx(tx)
        pass


# -*- coding: utf-8 -*-

"""Main module."""

import json
import base58

from . import account as acc
from . import comm
from .obj import block
from .obj import transaction
from .obj import address as addr
from .obj import block_hash as bh
from .obj import peer as pr
from .errors.exception import CommunicationException
from .status.commit_status import CommitStatus
from .utils.converter import convert_commit_result_to_json
from .utils.encoding import encode_address, decode_address, encode_private_key, decode_private_key


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

    @account.setter
    def account(self, a):
        self.__account = a

    def new_account(self, password=None, private_key=None):
        self.__account = acc.Account(password, private_key)
        if private_key is not None:
            self.get_account()
        return self.__account

    # TODO how about making account_state class,
    #       or how about returning account and change method name
    def get_account(self, address=None):
        """
        Return the account of `address`.
        :param address:
        :return:
        """
        if self.__comm is None:
            return None

        self_acc = False
        if address is None:
            address = self.__account.address.get_address_bytes()
            self_acc = True
        elif isinstance(address, str):
            address = decode_address(address)
        elif type(address) is addr.Address:
            address = bytes(address)

        try:
            state = self.__comm.get_account_state(address)
        except Exception as e:
            raise CommunicationException(e) from e

        if self_acc:
            self.__account.state = state
            account = self.__account
        else:
            account = acc.Account("", empty=True)
            account.state = state
            account.address = address

        return account

    def connect(self, target):
        """
        Connect to the gRPC server running on port `target` e.g. target="localhost:7845".
        :param target:
        :return:
        """
        if target is None:
            raise ValueError('need target value')

        self.__comm = comm.Comm(target)
        try:
            self.__comm.connect()
        except Exception as e:
            raise CommunicationException(e) from e

    def disconnect(self):
        """
        Disconnect from the gRPC server.
        """
        if self.__comm is not None:
            try:
                self.__comm.disconnect()
            except Exception as e:
                raise CommunicationException(e) from e

    def get_blockchain_status(self):
        """
        Returns the highest block hash and block height so far.
        :return:
        """
        if self.__comm is None:
            return None, -1

        try:
            status = self.__comm.get_blockchain_status()
        except Exception as e:
            raise CommunicationException(e) from e

        return bh.BlockHash(status.best_block_hash), status.best_height

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
            if type(block_hash) is not bh.BlockHash:
                block_hash = bh.BlockHash(block_hash)
            query = block_hash.value

        try:
            result = self.__comm.get_block(query)
        except Exception as e:
            raise CommunicationException(e) from e

        b = block.Block(grpc_block=result)
        return b

    def get_node_accounts(self, skip_state=False):
        """
        Returns a list of all node accounts.
        :return:
        """

        try:
            result = self.__comm.get_accounts()
        except Exception as e:
            raise CommunicationException(e) from e

        accounts = []
        for a in result.accounts:
            if skip_state:
                account = acc.Account("", empty=True)
                account.address = a.address
            else:
                account = self.get_account(a.address)
            accounts.append(account)

        return accounts

    def get_peers(self):
        """
        Returns a list of peers.
        :return:
        """
        try:
            result = self.__comm.get_peers()
        except Exception as e:
            raise CommunicationException(e) from e

        peers = []
        for i in range(len(result.peers)):
            p = result.peers[i]
            s = result.states[i]
            peer = pr.Peer()
            peer.info = p
            peer.state = s
            peers.append(peer)

        return peers

    def get_node_state(self, timeout=1):
        """
        Returns information about the node state.
        :return:
        """
        try:
            result = self.__comm.get_node_state(timeout)
        except Exception as e:
            raise CommunicationException(e) from e

        json_txt = result.value.decode('utf8').replace("'", '"')
        return json.loads(json_txt)

    def get_tx(self, tx_hash):
        """
        Returns info on transaction with hash `tx_hash`.
        :param tx_hash:
        :return:
        """
        try:
            result = self.__comm.get_tx(tx_hash)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def lock_account(self, address, passphrase):
        """
        Locks the account with address `address` with the passphrase `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        try:
            result = self.__comm.lock_account(address, passphrase)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def unlock_account(self, address, passphrase):
        """
        Unlocks the account with address `address` with the passphrase `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        try:
            result = self.__comm.unlock_account(address=address, passphrase=passphrase)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def _send_payload(self, account, to_address, nonce, amount, fee_limit, fee_price, payload):
        tx = transaction.Transaction(from_address=bytes(account.address),
                                     to_address=to_address,
                                     nonce=nonce, amount=amount,
                                     fee_limit=fee_limit, fee_price=fee_price,
                                     payload=payload)
        tx.sign = account.sign_msg_hash(tx.calculate_hash(including_sign=False))
        return self.send_tx(tx)

    def send_payload(self, amount, payload, to_address=None, retry_nonce=0):
        if self.__comm is None:
            return None, None

        if isinstance(to_address, str):
            to_address = decode_address(to_address)

        nonce = self.__account.nonce + 1
        signed_txs, results = self._send_payload(account=self.__account,
                                                 to_address=to_address,
                                                 nonce=nonce, amount=amount,
                                                 fee_limit=0, fee_price=0,
                                                 payload=payload)

        while retry_nonce >= 0:
            retry_nonce -= 1

            es = int(results[0]['error_status'])
            if es == CommitStatus.TX_HAS_SAME_NONCE:
                nonce += 1
                signed_txs, results = self._send_payload(account=self.__account,
                                                         to_address=to_address,
                                                         nonce=nonce, amount=amount,
                                                         fee_limit=0, fee_price=0,
                                                         payload=payload)
            elif es == CommitStatus.TX_OK:
                self.__account.nonce = nonce
                break
            else:
                break

        return signed_txs[0], results[0]

    def send_unsigned_tx(self, unsigned_tx):
        """
        Sends the unsigned transaction.
        The unsigned transaction will be signed by the account
        which is stored in the connected node.
        :param unsigned_tx:
        :return:
        """
        try:
            result = self.__comm.send_tx(unsigned_tx)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def send_tx(self, signed_txs):
        """
        Send a set of signed transactions simultaneously.
        These transactions will push to the memory pool after verifying.
        :param signed_txs:
        :return:
        """
        if not isinstance(signed_txs, (list, tuple)):
            signed_txs = [signed_txs]

        try:
            result_list = self.__comm.commit_txs(signed_txs)
        except Exception as e:
            raise CommunicationException(e) from e

        results = []
        for r in result_list.results:
            results.append(convert_commit_result_to_json(r))
        return signed_txs, results

    def import_account(self, exported_data, password):
        if exported_data is None or 0 == len(exported_data):
            # TODO unit test + exception handling
            assert 1 == 0

        if password is None or 0 == len(password):
            # TODO unit test + exception handling
            assert 1 == 0

        if isinstance(exported_data, str):
            exported_data = decode_private_key(exported_data)

        if isinstance(password, bytes):
            password = password.decode('utf-8')

        self.__account = acc.Account.decrypt_account(exported_data, password)
        return self.__account

    def export_account(self, account=None):
        if account is None:
            account = self.__account

        enc_acc = acc.Account.encrypt_account(account)
        return encode_private_key(enc_acc)

    def get_tx_result(self, tx_hash):
        if self.__comm is None:
            return None

        if isinstance(tx_hash, str):
            tx_hash = base58.b58decode(tx_hash)

        try:
            result = self.__comm.get_receipt(tx_hash)
        except Exception as e:
            raise CommunicationException(e) from e

        return encode_address(result.contractAddress), result.status, result.ret

    def deploy_sc(self, payload, amount=0, args=None):
        if isinstance(payload, str):
            payload = decode_address(payload)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        payload_bytes = (len(payload) + 4).to_bytes(4, byteorder='little')
        payload_bytes += payload

        if args is not None and len(args) > 0:
            args_txt = "["
            for arg in args:
                args_txt += "\"" + arg + "\","
            args_txt[len(args_txt) - 1] = "]"

            payload_bytes += bytes(args_txt)

        tx, result = self.send_payload(amount=amount, payload=payload_bytes)
        return tx, result

    def call_sc(self, sc_address, func_name, amount=0, args=None):
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        payload_str = "{\"Name\":\"" + func_name + "\""
        if args is not None and len(args) > 0:
            payload_str += ", \"Args\":["
            for arg in args:
                payload_str += "\"" + arg + "\","
            p = list(payload_str)
            p[len(payload_str) - 1] = "]"
            payload_str = "".join(p)
        payload_str += "}"
        payload = payload_str.encode('utf-8')

        return self.send_payload(to_address=sc_address, amount=amount, payload=payload)

    def query_sc(self, sc_address, func_name, args=None):
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        payload_str = "{\"Name\":\"" + func_name + "\""
        if args is not None and len(args) > 0:
            payload_str += ", \"Args\":["
            for arg in args:
                payload_str += "\"" + arg + "\","
            p = list(payload_str)
            p[len(payload_str) - 1] = "]"
            payload_str = "".join(p)
        payload_str += "}"
        payload = payload_str.encode('utf-8')

        try:
            result = self.__comm.query_contract(sc_address, payload)
        except Exception as e:
            raise CommunicationException(e) from e

        return result.value

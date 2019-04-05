# -*- coding: utf-8 -*-

"""Main module."""

import json

from . import account as acc
from . import comm

from .obj import transaction
from .obj import address as addr
from .obj import block_hash as bh
from .obj import peer as pr
from .obj import tx_hash as th
from .obj.block import Block
from .obj.blockchain_info import BlockchainInfo
from .obj.blockchain_status import BlockchainStatus
from .obj.consensus_info import ConsensusInfo
from .obj.call_info import CallInfo
from .obj.event import Event
from .obj.event_stream import EventStream
from .obj.transaction import Transaction
from .obj.tx_hash import TxHash
from .obj.tx_result import TxResult
from .obj.sc_state import SCState, SCStateVar
from .obj.var_proof import VarProofs
from .obj.block_stream import BlockStream

from .errors.exception import CommunicationException
from .errors.general_exception import GeneralException

from .status.commit_status import CommitStatus

from .utils.encoding import decode_address, \
    encode_private_key, decode_private_key, decode_root, \
    encode_tx_hash, decode_tx_hash


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

    def new_account(self, private_key=None, skip_state=False):
        self.__account = acc.Account(private_key=private_key)
        if not skip_state:
            self.get_account()
        return self.__account

    # TODO how about making account_state class,
    #       or how about returning account and change method name
    def get_account(self, account=None, address=None, proof=False, root=b'', compressed=True):
        """
        Return account information
        :param address:
        :param proof:
        :param root:
        :param compressed:
        :return:
        """
        if self.__comm is None:
            return None

        if account is None and address is None:
            # self account
            ret_account = self.__account
            req_address = bytes(self.__account.address)
        elif account is not None:
            ret_account = account
            req_address = bytes(account.address)
        else:
            if address is None:
                raise GeneralException("Fail to get an account info. No designated account address.")
            else:
                ret_account = acc.Account(empty=True)
                if isinstance(address, str):
                    req_address = decode_address(address)
                elif type(address) is addr.Address:
                    req_address = bytes(address)
                else:
                    req_address = address
                ret_account.address = req_address

        if proof:
            if isinstance(root, str) and len(root) != 0:
                root = decode_root(root)
            try:
                state_proof = self.__comm.get_account_state_proof(req_address,
                                                                  root,
                                                                  compressed)
            except Exception as e:
                raise CommunicationException(e) from e

            ret_account.state = state_proof.state
            ret_account.state_proof = state_proof
        else:
            try:
                state = self.__comm.get_account_state(req_address)
            except Exception as e:
                raise CommunicationException(e) from e

            ret_account.state = state
            ret_account.state_proof = None

        return ret_account

    def connect(self, target):
        """
        Connect to the gRPC server running on port `target` e.g.
        target="localhost:7845".
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
        try:
            status = self.__comm.get_blockchain_status()
        except Exception as e:
            raise CommunicationException(e) from e
        self.chain_id = status.best_chain_id_hash

    def disconnect(self):
        """
        Disconnect from the gRPC server.
        """
        if self.__comm is not None:
            try:
                self.__comm.disconnect()
            except Exception as e:
                raise CommunicationException(e) from e

    def get_chain_info(self, with_consensus_info=True):
        """
        Returns the blockchain info
        :return:
        """
        if self.__comm is None:
            return None

        try:
            chain_info = self.__comm.get_chain_info()
            if with_consensus_info:
                consensus_info = self.__comm.get_consensus_info()
            else:
                consensus_info = None
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockchainInfo(chain_info, consensus_info)

    def get_consensus_info(self):
        """
        Returns the consensus information
        :return:
        """
        if self.__comm is None:
            return None

        try:
            info = self.__comm.get_consensus_info()
        except Exception as e:
            raise CommunicationException(e) from e

        return ConsensusInfo(info)

    def get_status(self):
        """
        Returns the blockchain status
        :return:
        """
        if self.__comm is None:
            return None

        try:
            status = self.__comm.get_blockchain_status()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockchainStatus(status)

    def receive_block_meta_stream(self):
        """
        Returns the iterable block stream
        :return:
        """
        if self.__comm is None:
            return None

        try:
            stream = self.__comm.receive_block_meta_stream()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockStream(stream)

    def receive_block_stream(self):
        """
        Returns the iterable block stream
        :return:
        """
        if self.__comm is None:
            return None

        try:
            stream = self.__comm.receive_block_stream()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockStream(stream)

    def get_block_metas(self, block_hash=None, block_height=-1, list_size=20,
                        offset=0, is_asc_order=False):
        """
        Returns the list of blocks.
        :param block_hash:
        :param block_height:
        :param list_size: maximum number of results
        :param offset: the start point to search until the block_hash or block_height
        :param is_asc_order:
        :return:
        """
        if self.__comm is None:
            return None

        if block_hash is None and block_height < 0:
            raise ValueError("Please insert a block hash or height")

        try:
            bms = self.__comm.get_block_metas(block_hash=block_hash,
                                              block_height=block_height,
                                              list_size=list_size,
                                              offset=offset,
                                              is_asc_order=is_asc_order)
            block_headers = []
            for bm in bms.blocks:
                block_headers.append(Block(hash_value=bm.hash,
                                           grpc_block_header=bm.header,
                                           tx_cnt=bm.txcount))
        except Exception as e:
            raise CommunicationException(e) from e

        return block_headers

    def receive_event_stream(self, sc_address, event_name, start_block_no=0,
                             end_block_no=0, with_desc=False, arg_filter=None,
                             recent_block_cnt=0):
        if self.__comm is None:
            return None

        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)
        elif isinstance(sc_address, TxHash):
            sc_address = bytes(sc_address)

        if arg_filter:
            if isinstance(arg_filter, (dict, list, tuple)):
                arg_filter = json.dumps(arg_filter)
            arg_filter = arg_filter.encode('utf-8')

        try:
            es = self.__comm.receive_event_stream(sc_address=sc_address,
                                                  event_name=event_name,
                                                  start_block_no=start_block_no,
                                                  end_block_no=end_block_no,
                                                  with_desc=with_desc,
                                                  arg_filter=arg_filter,
                                                  recent_block_cnt=recent_block_cnt)
        except Exception as e:
            raise CommunicationException(e) from e

        return EventStream(es)

    def get_events(self, sc_address, event_name, start_block_no=-1,
                   end_block_no=-1, with_desc=False, arg_filter=None,
                   recent_block_cnt=0):
        if self.__comm is None:
            return None

        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)
        elif isinstance(sc_address, TxHash):
            sc_address = bytes(sc_address)

        if arg_filter:
            if isinstance(arg_filter, (dict, list, tuple)):
                arg_filter = json.dumps(arg_filter)
            arg_filter = arg_filter.encode('utf-8')

        # max range = 10000
        if start_block_no < 0 and end_block_no < 0:
            recent_block_cnt = 10000
        elif start_block_no < 0:
            start_block_no = end_block_no - 10000
            if start_block_no < 0:
                start_block_no = 0
        elif end_block_no < 0:
            end_block_no = start_block_no + 10000

        try:
            result = self.__comm.get_events(sc_address=sc_address,
                                            event_name=event_name,
                                            start_block_no=start_block_no,
                                            end_block_no=end_block_no,
                                            with_desc=with_desc,
                                            arg_filter=arg_filter,
                                            recent_block_cnt=recent_block_cnt)
            event_list = []
            for e in result.events:
                event_list.append(Event(e))
        except Exception as e:
            raise CommunicationException(e) from e

        return event_list

    def get_block_headers(self, block_hash=None, block_height=-1, list_size=20,
                          offset=0, is_asc_order=False):
        """
        Returns the list of blocks.
        :param block_hash:
        :param block_height:
        :param list_size: maximum number of results
        :param offset: the start point to search until the block_hash or block_height
        :param is_asc_order:
        :return:
        """
        if self.__comm is None:
            return None

        if block_hash is None and block_height < 0:
            raise ValueError("Please insert a block hash or height")

        try:
            bhs = self.__comm.get_block_headers(block_hash=block_hash,
                                                block_height=block_height,
                                                list_size=list_size,
                                                offset=offset,
                                                is_asc_order=is_asc_order)
            block_headers = []
            for b in bhs.blocks:
                block_headers.append(Block(grpc_block=b))
        except Exception as e:
            raise CommunicationException(e) from e

        return block_headers

    def get_blockchain_status(self):
        """
        Returns the highest block hash and block height so far.
        :return:
        """
        status = self.get_status()
        return status.best_block_hash, status.best_block_height

    def get_block(self, block_hash=None, block_height=-1):
        """
        Returns information about block `block_hash`.
        :param block_hash:
        :param block_height:
        :return:
        """
        if self.__comm is None:
            return None

        if block_height >= 0:
            query = block_height.to_bytes(8, byteorder='little')
        else:
            if type(block_hash) is not bh.BlockHash:
                block_hash = bh.BlockHash(block_hash)
            query = block_hash.value

        try:
            result = self.__comm.get_block(query)
        except Exception as e:
            raise CommunicationException(e) from e

        b = Block(grpc_block=result)
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
                account = acc.Account(empty=True)
                account.address = a.address
            else:
                account = self.get_account(address=a.address)
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
        for i, p in enumerate(result.peers):
            peer = pr.Peer()
            peer.info = p
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

    def get_tx(self, tx_hash, mempool_only=False, skip_block=False):
        """
        Returns info on transaction with hash `tx_hash`.
        :param tx_hash:
        :return:
        """
        if isinstance(tx_hash, str):
            tx_hash = decode_tx_hash(tx_hash)
        elif type(tx_hash) == TxHash:
            tx_hash = bytes(tx_hash)

        result_tx = None
        result_tx_block_hash = None
        result_tx_index = None
        result_tx_is_in_mempool = False

        try:
            result_tx = self.__comm.get_tx(tx_hash)
            result_tx_block_hash = None
            result_tx_index = None
            result_tx_is_in_mempool = True
            get_result = True
        except Exception as e:
            if mempool_only:
                raise CommunicationException(e) from e
            else:
                get_result = False

        if not get_result:
            try:
                result = self.__comm.get_block_tx(tx_hash)
                result_tx = result.tx
                result_tx_block_hash = result.txIdx.blockHash
                result_tx_index = result.txIdx.idx
                result_tx_is_in_mempool = False
            except Exception as e:
                raise CommunicationException(e) from e

        if result_tx_block_hash is not None:
            if skip_block:
                result_tx_block = Block(hash_value=result_tx_block_hash,
                                        height=None)
            else:
                result_tx_block = self.get_block(block_hash=result_tx_block_hash)
        else:
            result_tx_block = None

        from_address = addr.Address(None, empty=True)
        from_address.value = result_tx.body.account
        to_address = addr.Address(None, empty=True)
        to_address.value = result_tx.body.recipient

        tx = Transaction(read_only=True,
                         tx_hash=result_tx.hash,
                         nonce=result_tx.body.nonce,
                         from_address=from_address,
                         to_address=to_address,
                         amount=result_tx.body.amount,
                         payload=result_tx.body.payload,
                         fee_price=result_tx.body.gasPrice,
                         fee_limit=result_tx.body.gasLimit,
                         tx_sign=result_tx.body.sign,
                         tx_type=result_tx.body.type,
                         chain_id=result_tx.body.chainIdHash,
                         block=result_tx_block, index_in_block=result_tx_index,
                         is_in_mempool=result_tx_is_in_mempool)

        return tx

    def lock_account(self, address, passphrase):
        """
        Locks the account with address `address` with the passphrase
        `passphrase`.
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
        Unlocks the account with address `address` with the passphrase
        `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        try:
            result = self.__comm.unlock_account(address=address,
                                                passphrase=passphrase)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def generate_tx(self, to_address, nonce, amount, fee_limit=0, fee_price=0, payload=None):
        if to_address is not None:
            address = addr.Address(None, empty=True)
            address.value = to_address
            to_address = address

        tx = transaction.Transaction(from_address=self.__account.address,
                                     to_address=to_address,
                                     nonce=nonce, amount=amount,
                                     fee_limit=fee_limit, fee_price=fee_price,
                                     payload=payload, chain_id=self.chain_id)
        tx.sign = self.__account.sign_msg_hash(tx.calculate_hash(including_sign=False))
        return tx

    def send_payload(self, amount, payload, to_address=None, retry_nonce=0):
        if self.__comm is None:
            return None, None

        if isinstance(to_address, str):
            to_address = decode_address(to_address)

        nonce = self.__account.nonce + 1
        tx = self.generate_tx(to_address=to_address,
                              nonce=nonce, amount=amount,
                              fee_limit=0, fee_price=0,
                              payload=payload)
        signed_tx, result = self.send_tx(signed_tx=tx)

        if result.status == CommitStatus.TX_OK:
            self.__account.nonce = nonce
        elif result.status == CommitStatus.TX_HAS_SAME_NONCE:
            while retry_nonce > 0:
                retry_nonce -= 1

                nonce += 1
                tx = self.generate_tx(to_address=to_address,
                                      nonce=nonce, amount=amount,
                                      fee_limit=0, fee_price=0,
                                      payload=payload)
                signed_tx, result = self.send_tx(signed_tx=tx)

                es = result.status
                if es == CommitStatus.TX_OK:
                    self.__account.nonce = nonce
                    break
                elif es != CommitStatus.TX_HAS_SAME_NONCE:
                    break

        return signed_tx, result

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

    def send_tx(self, signed_tx):
        """
        Send a signed transaction.
        This transaction will push to the memory pool after verifying.
        :param signed_tx:
        :return:
        """
        signed_txs, results = self.batch_tx(signed_txs=[signed_tx])
        return signed_txs[0], results[0]

    def batch_tx(self, signed_txs):
        """
        Send a set of signed transactions simultaneously.
        These transactions will push to the memory pool after verifying.
        :param signed_txs:
        :return:
        """
        try:
            result_list = self.__comm.commit_txs(signed_txs)
        except Exception as e:
            raise CommunicationException(e) from e

        results = []
        for i, r in enumerate(result_list.results):
            tx_result = TxResult(tx=signed_txs[i], result=result_list.results[i])
            if tx_result.status == CommitStatus.TX_OK:
                self.__account.nonce += 1
            results.append(tx_result)
        return signed_txs, results

    def import_account(self, exported_data, password, skip_state=False, skip_self=False):
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

        account = acc.Account.decrypt_account(exported_data, password)
        if not skip_self:
            self.__account = account
            if not skip_state:
                self.get_account()
        else:
            if not skip_state:
                self.get_account(account=account)
        return account

    def export_account(self, password, account=None):
        if account is None:
            account = self.__account

        enc_acc = acc.Account.encrypt_account(account, password)
        return encode_private_key(enc_acc)

    def get_tx_result(self, tx_hash):
        if self.__comm is None:
            return None

        if isinstance(tx_hash, str):
            tx_hash = decode_tx_hash(tx_hash)
        elif type(tx_hash) is th.TxHash:
            tx_hash = bytes(tx_hash)

        try:
            result = self.__comm.get_receipt(tx_hash)
            tx_result = TxResult(result=result)
            tx_result.tx_id = encode_tx_hash(tx_hash)
        except Exception as e:
            raise CommunicationException(e) from e

        return tx_result

    def deploy_sc(self, payload, amount=0, args=None, retry_nonce=0):
        if isinstance(payload, str):
            payload = decode_address(payload)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        payload_bytes = (len(payload) + 4).to_bytes(4, byteorder='little')
        payload_bytes += payload

        json_args = json.dumps(args, separators=(',', ':'))
        payload_bytes += json_args.encode('utf-8')

        tx, result = self.send_payload(amount=amount, payload=payload_bytes,
                                       retry_nonce=retry_nonce)
        return tx, result

    def new_call_sc_tx(self, sc_address, func_name, amount=0, args=None, nonce=None):
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        call_info = CallInfo(func_name, args).__dict__
        payload = json.dumps(call_info, separators=(',', ':')).encode('utf-8')

        if nonce is None:
            nonce = self.__account.nonce + 1

        return self.generate_tx(to_address=sc_address,
                                nonce=nonce, amount=amount,
                                fee_limit=0, fee_price=0, payload=payload)

    def batch_call_sc(self, sc_txs):
        return self.batch_tx(sc_txs)

    def call_sc(self, sc_address, func_name, amount=0, args=None):
        sc_tx = self.new_call_sc_tx(sc_address=sc_address, func_name=func_name,
                                    amount=amount, args=args)
        sc_txs, results = self.batch_call_sc([sc_tx])
        return sc_txs[0], results[0]

    def query_sc(self, sc_address, func_name, args=None):
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        call_info = CallInfo(func_name, args).__dict__
        payload = json.dumps(call_info, separators=(',', ':')).encode('utf-8')

        try:
            result = self.__comm.query_contract(sc_address, payload)
        except Exception as e:
            raise CommunicationException(e) from e

        return result.value

    def query_sc_state(self, sc_address, storage_keys, root=b'',
                       compressed=True):
        """ query_sc_state returns a SCState object containing the contract
        state and variable state with their respective merkle proofs.
        """
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = decode_address(sc_address)

        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)

        # convert SCStateVar objects to trie storage key strings
        storage_keys = [str(key) for key in storage_keys]

        try:
            result = self.__comm.query_contract_state(sc_address, storage_keys,
                                                      root, compressed)
        except Exception as e:
            raise CommunicationException(e) from e

        account = acc.Account(empty=True)
        account.state = result.contractProof.state
        account.state_proof = result.contractProof
        account.address = sc_address

        var_proofs = VarProofs(result.varProofs)

        return SCState(account=account, var_proofs=var_proofs)

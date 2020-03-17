# -*- coding: utf-8 -*-

"""Main module."""

import hashlib
import json
import time
import asyncio
from typing import (
    Optional,
    Union,
    List,
    Dict,
    Tuple,
    Any
)

from . import account as acc
from . import comm

from .obj import address as addr
from .obj import block_hash as bh
from .obj import peer as pr
from .obj import tx_hash as th
from .obj.block import Block
from .obj.block_stream import BlockStream
from .obj.blockchain_info import BlockchainInfo
from .obj.blockchain_status import BlockchainStatus
from .obj.call_info import CallInfo
from .obj.change_conf_info import ChangeConfInfo
from .obj.consensus_info import ConsensusInfo
from .obj.event import Event
from .obj.event_stream import EventStream
from .obj.name_info import NameInfo
from .obj.node_info import NodeInfo
from .obj.sc_state import (
    SCState,
    SCStateVar
)
from .obj.transaction import Transaction, TxType
from .obj.tx_hash import TxHash
from .obj.tx_result import TxResult
from .obj.var_proof import VarProofs
from .obj.abi import Abi
from .obj.enterprise_config import EnterpriseConfig

from .errors.exception import CommunicationException
from .errors.general_exception import GeneralException

from .status.commit_status import CommitStatus

from .utils.encoding import (
    decode_address,
    decode_contract_code,
    encode_private_key,
    decode_private_key,
    decode_root,
    encode_tx_hash,
    decode_tx_hash
)


class Aergo:
    """
    Main class for `herapy <http://github.com/aergoio/herapy>`_
    """
    def __init__(self) -> None:
        self.__account: Optional[acc.Account] = None
        self.__comm: Optional[comm.Comm] = None

    @property
    def account(self) -> Optional[acc.Account]:
        """
        Returns the account object.
        :return:
        """
        return self.__account

    @account.setter
    def account(self, a: acc.Account) -> None:
        self.__account = a

    def new_account(
        self,
        private_key: Union[str, bytes, None] = None,
        skip_state: bool = False
    ) -> acc.Account:
        self.__account = acc.Account(private_key=private_key)
        if not skip_state:
            self.get_account()
        return self.__account

    # TODO how about making account_state class,
    #       or how about returning account and change method name
    def get_account(
        self,
        account: Optional[acc.Account] = None,
        address: Union[str, bytes, addr.Address, None] = None,
        proof: bool = False,
        root: bytes = b'',
        compressed: bool = True
    ) -> acc.Account:
        """
        Return account information
        :param address:
        :param proof:
        :param root:
        :param compressed:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if account is None and address is None:
            # self account
            ret_account = self.__account
            if ret_account is None or ret_account.address is None:
                raise GeneralException(
                    "Current account is not set")
            req_address = bytes(ret_account.address)
        elif account is not None:
            ret_account = account
            if account.address is None:
                raise GeneralException(
                    "Provided account address is not set")
            req_address = bytes(account.address)
        else:
            if address is None:
                raise GeneralException(
                    "Fail to get an account info. No designated account "
                    "address."
                )
            else:
                ret_account = acc.Account(empty=True)
                if isinstance(address, str):
                    req_address = addr.Address.decode(address)
                elif isinstance(address, addr.Address):
                    req_address = bytes(address)
                else:
                    req_address = address
                ret_account.address = req_address  # type: ignore

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

    def connect(
        self,
        target: str,
        tls_ca_cert: Optional[str] = None,
        tls_cert: Optional[str] = None,
        tls_key: Optional[str] = None
    ) -> None:
        """
        Connect to the gRPC server running on port `target` e.g.
        target="localhost:7845".
        :param target:
        :param tls_ca_cert:
        :param tls_cert:
        :param tls_key:
        :return:
        """
        if target is None:
            raise ValueError('need target value')

        tls_ca_cert_bytes: Optional[bytes] = None
        tls_cert_bytes: Optional[bytes] = None
        tls_key_bytes: Optional[bytes] = None
        if tls_ca_cert is not None:
            try:
                with open(tls_ca_cert, 'rb') as f:
                    tls_ca_cert_bytes = f.read()
            except:
                pass
        if tls_cert is not None:
            try:
                with open(tls_cert, 'rb') as f:
                    tls_cert_bytes = f.read()
            except:
                pass
        if tls_key is not None:
            try:
                with open(tls_key, 'rb') as f:
                    tls_key_bytes = f.read()
            except:
                pass

        self.__comm = comm.Comm(
            target, tls_ca_cert_bytes, tls_cert_bytes, tls_key_bytes)
        try:
            self.__comm.connect()
        except Exception as e:
            raise CommunicationException(e) from e
        try:
            status = self.__comm.get_blockchain_status()
        except Exception as e:
            raise CommunicationException(e) from e
        self.chain_id = status.best_chain_id_hash

    def disconnect(self) -> None:
        """
        Disconnect from the gRPC server.
        """
        if self.__comm is not None:
            try:
                self.__comm.disconnect()
            except Exception as e:
                raise CommunicationException(e) from e

    def get_chain_info(
        self,
        with_consensus_info: bool = True
    ) -> BlockchainInfo:
        """
        Returns the blockchain info
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            chain_info = self.__comm.get_chain_info()
            if with_consensus_info:
                consensus_info = self.__comm.get_consensus_info()
            else:
                consensus_info = None
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockchainInfo(chain_info, consensus_info)

    def get_consensus_info(self) -> ConsensusInfo:
        """
        Returns the consensus information
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            info = self.__comm.get_consensus_info()
        except Exception as e:
            raise CommunicationException(e) from e

        return ConsensusInfo(info)

    def get_status(self) -> BlockchainStatus:
        """
        Returns the blockchain status
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            status = self.__comm.get_blockchain_status()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockchainStatus(status)

    def receive_block_meta_stream(self) -> BlockStream:
        """
        Returns the iterable block stream
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            stream = self.__comm.receive_block_meta_stream()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockStream(stream)

    def receive_block_stream(self) -> BlockStream:
        """
        Returns the iterable block stream
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            stream = self.__comm.receive_block_stream()
        except Exception as e:
            raise CommunicationException(e) from e

        return BlockStream(stream)

    def get_block_metas(
        self,
        block_hash: Optional[bytes] = None,
        block_height: int = -1,
        list_size: int = 20,
        offset: int = 0,
        is_asc_order: bool = False
    ) -> List[Block]:
        """
        Returns the list of metadata of queried blocks.
        :param block_hash:
        :param block_height:
        :param list_size: maximum number of results
        :param offset: the start point to search until the block_hash or
        block_height
        :param is_asc_order:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

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
                                           tx_cnt=bm.txcount,
                                           size=bm.size))
        except Exception as e:
            raise CommunicationException(e) from e

        return block_headers

    def receive_event_stream(
        self,
        sc_address: Union[str, bytes, TxHash],
        event_name: str,
        start_block_no: int = 0,
        end_block_no: int = 0,
        with_desc: bool = False,
        arg_filter: Optional[Union[str, Dict, List, Tuple]] = None,
        recent_block_cnt: int = 0
    ) -> EventStream:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = addr.Address.decode(sc_address)
        elif isinstance(sc_address, TxHash):
            sc_address = bytes(sc_address)

        arg_filter_bytes: Optional[bytes] = None
        if arg_filter:
            if isinstance(arg_filter, (dict, list, tuple)):
                arg_filter = json.dumps(arg_filter)
            arg_filter_bytes = arg_filter.encode('utf-8')

        try:
            es = self.__comm.receive_event_stream(
                sc_address=sc_address, event_name=event_name,
                start_block_no=start_block_no, end_block_no=end_block_no,
                with_desc=with_desc, arg_filter=arg_filter_bytes,
                recent_block_cnt=recent_block_cnt
            )
        except Exception as e:
            raise CommunicationException(e) from e

        return EventStream(es)

    def get_events(
        self,
        sc_address: Union[bytes, str, TxHash],
        event_name: str,
        start_block_no: int = -1,
        end_block_no: int = -1,
        with_desc: bool = False,
        arg_filter: Optional[Union[str, Dict, List, Tuple]] = None,
        recent_block_cnt: int = 0
    ) -> List[Event]:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = addr.Address.decode(sc_address)
        elif isinstance(sc_address, TxHash):
            sc_address = bytes(sc_address)

        arg_filter_bytes: Optional[bytes] = None
        if arg_filter:
            if isinstance(arg_filter, (dict, list, tuple)):
                arg_filter = json.dumps(arg_filter)
            arg_filter_bytes = arg_filter.encode('utf-8')

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
                                            arg_filter=arg_filter_bytes,
                                            recent_block_cnt=recent_block_cnt)
            event_list = []
            for e in result.events:
                event_list.append(Event(e))
        except Exception as e:
            raise CommunicationException(e) from e

        return event_list

    def get_block_headers(
        self,
        block_hash: Optional[bytes] = None,
        block_height: int = -1,
        list_size: int = 20,
        offset: int = 0,
        is_asc_order: bool = False
    ) -> List[Block]:
        """
        Returns the list of blocks.
        :param block_hash:
        :param block_height:
        :param list_size: maximum number of results
        :param offset: the start point to search until the block_hash or
        block_height
        :param is_asc_order:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

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

    def get_blockchain_status(self) -> Tuple[bh.BlockHash, int]:
        """
        Returns the highest block hash and block height so far.
        :return:
        """
        status = self.get_status()
        return status.best_block_hash, status.best_block_height

    def get_block(
        self,
        block_hash: Union[bytes, bh.BlockHash, None] = None,
        block_height: int = -1
    ) -> Block:
        """
        Returns block information for `block_hash` or `block_height`.
        :param block_hash:
        :param block_height:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if block_height >= 0:
            query = block_height.to_bytes(8, byteorder='little')
        else:
            if block_hash is None:
                raise ValueError("Please insert a block hash or height")
            if not isinstance(block_hash, bh.BlockHash):
                block_hash = bh.BlockHash(block_hash)
            query = block_hash.value

        try:
            result = self.__comm.get_block(query)
        except Exception as e:
            raise CommunicationException(e) from e

        b = Block(grpc_block=result)
        return b

    def get_block_meta(
        self,
        block_hash: Union[bytes, bh.BlockHash, None] = None,
        block_height: int = -1
    ) -> Block:
        """
        Returns block metadata for `block_hash` or `block_height`.
        :param block_hash:
        :param block_height:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if block_height >= 0:
            query = block_height.to_bytes(8, byteorder='little')
        else:
            if block_hash is None:
                raise ValueError("Please insert a block hash or height")
            if not isinstance(block_hash, bh.BlockHash):
                block_hash = bh.BlockHash(block_hash)
            query = block_hash.value

        try:
            bm = self.__comm.get_block_meta(query)
        except Exception as e:
            raise CommunicationException(e) from e

        b = Block(hash_value=bm.hash,
                  grpc_block_header=bm.header,
                  tx_cnt=bm.txcount,
                  size=bm.size)
        return b

    def get_node_accounts(
        self,
        skip_state: bool = False
    ) -> List[acc.Account]:
        """
        Returns a list of all node accounts.
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

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

    def get_peers(self) -> List[pr.Peer]:
        """
        Returns a list of peers.
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

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

    def get_node_info(self, keys: Optional[str] = None) -> NodeInfo:
        """
        Returns the consensus information
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            info = self.__comm.get_node_info(keys)
        except Exception as e:
            raise CommunicationException(e) from e

        return NodeInfo(info)

    def get_node_state(self, timeout: int = 1) -> Dict:
        """
        Returns information about the node state.
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        try:
            result = self.__comm.get_node_state(timeout)
        except Exception as e:
            raise CommunicationException(e) from e

        json_txt = result.value.decode('utf8').replace("'", '"')
        return json.loads(json_txt)

    def get_tx(
        self,
        tx_hash: Union[str, TxHash, bytes],
        mempool_only: bool = False,
        skip_block: bool = False
    ) -> Transaction:
        """
        Returns info on transaction with hash `tx_hash`.
        :param tx_hash:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if isinstance(tx_hash, str):
            tx_hash_bytes = decode_tx_hash(tx_hash)
            assert tx_hash_bytes
            tx_hash = tx_hash_bytes
        elif isinstance(tx_hash, TxHash):
            tx_hash = bytes(tx_hash)

        try:
            result_tx = self.__comm.get_tx(tx_hash)
            result_tx_block_hash = None
            result_tx_index = -1
            result_tx_is_in_mempool = True
        except Exception as e:
            if mempool_only:
                raise CommunicationException(e) from e
            else:
                try:
                    result = self.__comm.get_block_tx(tx_hash)
                    result_tx = result.tx
                    result_tx_block_hash = result.txIdx.blockHash
                    result_tx_index = result.txIdx.idx
                    result_tx_is_in_mempool = False
                except Exception as e:
                    raise CommunicationException(e) from e

        result_tx_block: Optional[Block]
        if result_tx_block_hash is not None:
            if skip_block:
                result_tx_block = Block(hash_value=result_tx_block_hash,
                                        height=None)
            else:
                result_tx_block = self.get_block(
                    block_hash=result_tx_block_hash)
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
                         gas_price=result_tx.body.gasPrice,
                         gas_limit=result_tx.body.gasLimit,
                         tx_sign=result_tx.body.sign,
                         tx_type=result_tx.body.type,
                         chain_id=result_tx.body.chainIdHash,
                         block=result_tx_block, index_in_block=result_tx_index,
                         is_in_mempool=result_tx_is_in_mempool)

        return tx

    def lock_account(self, address: bytes, passphrase: str):
        """
        Locks the account with address `address` with the passphrase
        `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        try:
            result = self.__comm.lock_account(address, passphrase)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def unlock_account(self, address: bytes, passphrase: str):
        """
        Unlocks the account with address `address` with the passphrase
        `passphrase`.
        :param address:
        :param passphrase:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        try:
            result = self.__comm.unlock_account(address=address,
                                                passphrase=passphrase)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def generate_tx(
        self,
        to_address: Union[bytes, str, None],
        nonce: int,
        amount: Union[bytes, str, int, float],
        gas_limit: int = 0,
        gas_price: int = 0,
        payload: Optional[bytes] = None,
        tx_type: TxType = TxType.NORMAL
    ) -> Transaction:
        if self.__account is None:
            raise GeneralException("Current account is not set")
        address_obj: Optional[addr.Address] = None
        if to_address is not None:
            address_obj = addr.Address(None, empty=True)
            address_obj.value = to_address  # type: ignore

        tx = Transaction(
            tx_type=tx_type, from_address=self.__account.address,
            to_address=address_obj, nonce=nonce, amount=amount,
            gas_limit=gas_limit, gas_price=gas_price, payload=payload,
            chain_id=self.chain_id
        )
        tx.sign = self.__account.sign_msg_hash(
            tx.calculate_hash(including_sign=False))
        return tx

    def transfer(
        self,
        to_address: Union[str, bytes, addr.Address, addr.GovernanceTxAddress],
        amount: Union[bytes, str, int, float],
        retry_nonce: int = 3
    ) -> Tuple[Transaction, TxResult]:
        return self.send_payload(
            amount=amount, to_address=to_address, payload=None,
            retry_nonce=retry_nonce
        )

    def send_payload(
        self,
        amount: Union[bytes, str, int, float],
        payload: Optional[bytes] = None,
        to_address: Union[str, bytes, addr.Address, addr.GovernanceTxAddress,
                          None] = None,
        retry_nonce: int = 0,
        tx_type: TxType = TxType.TRANSFER,
        gas_limit: int = 0,
        gas_price: int = 0
    ) -> Tuple[Transaction, TxResult]:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if self.__account is None:
            raise GeneralException("Current account is not set")

        to_address_bytes: Optional[bytes]
        if isinstance(to_address, str):
            # check address type
            address_type = addr.check_name_address(to_address)
            if address_type > 0:
                to_address_bytes = to_address.encode()
                if 2 == address_type:
                    tx_type = TxType.GOVERNANCE
            else:
                try:
                    to_address_bytes = decode_address(to_address)
                except Exception as e:
                    raise ValueError("Invalid receiver address: {}".format(e))
        elif isinstance(to_address, addr.Address):
            to_address_bytes = bytes(to_address)
        elif isinstance(to_address, addr.GovernanceTxAddress):
            if addr.check_name_address(to_address.value):
                to_address_bytes = to_address.value.encode()
                tx_type = TxType.GOVERNANCE
        else:
            to_address_bytes = to_address

        nonce = self.__account.nonce + 1
        tx = self.generate_tx(to_address=to_address_bytes,
                              nonce=nonce, amount=amount,
                              gas_limit=gas_limit, gas_price=gas_price,
                              payload=payload, tx_type=tx_type)
        signed_tx, result = self.send_tx(signed_tx=tx)

        if result.status == CommitStatus.TX_OK:
            self.__account.nonce = nonce
        elif result.status == CommitStatus.TX_HAS_SAME_NONCE:
            while retry_nonce > 0:
                retry_nonce -= 1

                # update account info.
                self.get_account()
                new_nonce = self.__account.nonce + 1
                if new_nonce == nonce:
                    nonce += 1
                else:
                    nonce = new_nonce

                tx = self.generate_tx(to_address=to_address_bytes,
                                      nonce=nonce, amount=amount,
                                      gas_limit=gas_limit, gas_price=gas_price,
                                      payload=payload, tx_type=tx_type)
                signed_tx, result = self.send_tx(signed_tx=tx)

                es = result.status
                if es == CommitStatus.TX_OK:
                    self.__account.nonce = nonce
                    break
                elif es != CommitStatus.TX_HAS_SAME_NONCE:
                    break

        return signed_tx, result

    def send_unsigned_tx(self, unsigned_tx: Transaction):
        """
        Sends the unsigned transaction.
        The unsigned transaction will be signed by the account
        which is stored in the connected node.
        :param unsigned_tx:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        try:
            result = self.__comm.send_tx(unsigned_tx)
        except Exception as e:
            raise CommunicationException(e) from e

        return result

    def send_tx(self, signed_tx: Transaction) -> Tuple[Transaction, TxResult]:
        """
        Send a signed transaction.
        This transaction will push to the memory pool after verifying.
        :param signed_tx:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        signed_txs, results = self.batch_tx(signed_txs=[signed_tx])
        return signed_txs[0], results[0]

    def batch_tx(
        self,
        signed_txs: List[Transaction]
    ) -> Tuple[List[Transaction], List[TxResult]]:
        """
        Send a set of signed transactions simultaneously.
        These transactions will push to the memory pool after verifying.
        :param signed_txs:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if self.__account is None:
            raise GeneralException("Current account is not set")
        try:
            result_list = self.__comm.commit_txs(signed_txs)
        except Exception as e:
            raise CommunicationException(e) from e

        results = []
        for i, r in enumerate(result_list.results):
            tx_result = TxResult(
                tx=signed_txs[i], result=result_list.results[i])
            if tx_result.status == CommitStatus.TX_OK:
                self.__account.nonce += 1
            results.append(tx_result)
        return signed_txs, results

    def import_account(
        self,
        exported_data: Union[str, bytes],
        password: Union[str, bytes],
        skip_state: bool = False,
        skip_self: bool = False
    ) -> acc.Account:
        if exported_data is None or 0 == len(exported_data):
            # TODO unit test + exception handling
            assert 1 == 0

        if password is None or 0 == len(password):
            # TODO unit test + exception handling
            assert 1 == 0

        if isinstance(exported_data, str):
            exported_data_bytes = decode_private_key(exported_data)
            assert exported_data_bytes
            exported_data = exported_data_bytes

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

    def import_account_from_keystore(
        self,
        keystore: Union[Dict, str],
        password: str,
        skip_state: bool = False,
        skip_self: bool = False
    ) -> acc.Account:
        account = acc.Account.decrypt_from_keystore(keystore, password)
        if not skip_self:
            self.__account = account
            if not skip_state:
                self.get_account()
        else:
            if not skip_state:
                self.get_account(account=account)
        return account

    def import_account_from_keystore_file(
        self,
        keystore_path: str,
        password: str,
        skip_state: bool = False,
        skip_self: bool = False
    ) -> acc.Account:
        with open(keystore_path, "r") as f:
            keystore = f.read()
        return self.import_account_from_keystore(
            keystore, password, skip_state, skip_self)

    def export_account(
        self,
        password: Union[str, bytes],
        account: Optional[acc.Account] = None
    ) -> str:
        if account is None:
            account = self.__account
        if account is None:
            raise GeneralException("Current account is not set")

        enc_acc = acc.Account.encrypt_account(account, password)
        export_str = encode_private_key(enc_acc)
        assert export_str
        return export_str

    def export_account_to_keystore(
        self,
        password: str,
        account: Optional[acc.Account] = None,
        kdf_n: int = 2**18
    ) -> Dict:
        if account is None:
            account = self.__account
        if account is None:
            raise GeneralException("Current account is not set")

        keystore = acc.Account.encrypt_to_keystore(account, password, kdf_n)
        return keystore

    def export_account_to_keystore_file(
        self,
        keystore_path: str,
        password: str,
        account: Optional[acc.Account] = None,
        kdf_n: int = 2**18
    ) -> None:
        keystore = self.export_account_to_keystore(password, account, kdf_n)
        with open(keystore_path, 'w') as f:
            json.dump(keystore, f, indent=4)

    def get_tx_result(
        self,
        tx_hash: Union[str, th.TxHash, bytes]
    ) -> TxResult:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if isinstance(tx_hash, str):
            tx_hash_bytes = decode_tx_hash(tx_hash)
            assert tx_hash_bytes
            tx_hash = tx_hash_bytes
        elif isinstance(tx_hash, th.TxHash):
            tx_hash = bytes(tx_hash)

        try:
            result = self.__comm.get_receipt(tx_hash)
            tx_result = TxResult(result=result)
            tx_result.tx_id = encode_tx_hash(tx_hash)
        except Exception as e:
            raise CommunicationException(e) from e

        return tx_result

    def wait_tx_result(
        self,
        tx_hash: Union[str, th.TxHash, bytes],
        timeout: int = 30,
        tempo: float = 0.2
    ) -> TxResult:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if isinstance(tx_hash, str):
            tx_hash_bytes = decode_tx_hash(tx_hash)
            assert tx_hash_bytes
            tx_hash = tx_hash_bytes
        elif type(tx_hash) is th.TxHash:
            tx_hash = bytes(tx_hash)

        for _ in range(int(timeout / tempo) + 1):
            try:
                return self.get_tx_result(tx_hash)
            except CommunicationException as e:
                if (e.error_details is None
                        or e.error_details[:12] != "tx not found"):
                    raise e
            time.sleep(tempo)
        raise GeneralException("Transaction result not found")

    async def aio_wait_tx_result(
            self,
            tx_hash: Union[str, th.TxHash, bytes],
            timeout: int = 30,
            tempo: float = 0.2,
            result: Dict = None
    ) -> TxResult:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if isinstance(tx_hash, str):
            tx_hash_bytes = decode_tx_hash(tx_hash)
            assert tx_hash_bytes
            tx_hash = tx_hash_bytes
        elif type(tx_hash) is th.TxHash:
            tx_hash = bytes(tx_hash)

        for _ in range(int(timeout / tempo) + 1):
            try:
                tx_result = self.get_tx_result(tx_hash)
                if result is not None:
                    result['tx_result'] = tx_result
                return tx_result
            except CommunicationException as e:
                if (e.error_details is None
                        or e.error_details[:12] != "tx not found"):
                    raise e
            await asyncio.sleep(tempo)
        raise GeneralException("Transaction result not found")

    async def aio_wait_batch_result(
            self,
            txs: List[Union[str, th.TxHash, bytes, Transaction]],
            timeout: int = 30,
            tempo: float = 0.2,
            result: Dict = None
    ) -> List[TxResult]:
        coros = []
        for tx in txs:
            if isinstance(tx, Transaction):
                tx = tx.tx_hash

            coros.append(self.aio_wait_tx_result(tx, timeout, tempo))

        results = await asyncio.gather(*coros)
        if result is not None:
            result['tx_results'] = results

        return results

    def await_batch_result(
            self,
            txs: List[Union[str, th.TxHash, bytes, Transaction]],
            timeout: int = 30,
            tempo: float = 0.2
    ) -> Optional[List[TxResult]]:
        result: Dict[str, List[TxResult]] = {}
        asyncio.run(self.aio_wait_batch_result(txs, timeout, tempo, result))
        return result.get('tx_results')

    def deploy_sc(
        self,
        payload: Union[str, bytes],
        amount: Union[bytes, str, int, float] = 0,
        args: Optional[Any] = None,
        retry_nonce: int = 0,
        redeploy: bool = False,
        gas_limit: int = 0,
        gas_price: int = 0
    ):
        if isinstance(payload, str):
            payload = decode_contract_code(payload)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        payload_bytes = (len(payload) + 4).to_bytes(4, byteorder='little')
        payload_bytes += payload

        json_args = json.dumps(args, separators=(',', ':'))
        payload_bytes += json_args.encode('utf-8')

        if redeploy:
            tx_type = TxType.SC_REDEPLOY
        else:
            tx_type = TxType.SC_DEPLOY

        tx, result = self.send_payload(
            amount=amount, payload=payload_bytes, retry_nonce=retry_nonce,
            tx_type=tx_type, gas_limit=gas_limit, gas_price=gas_price
        )
        return tx, result

    def new_call_sc_tx(
        self,
        sc_address: Union[str, addr.GovernanceTxAddress, bytes],
        func_name: str,
        amount: int = 0,
        args: Optional[Any] = None,
        nonce: Optional[int] = None,
        gas_limit: int = 0,
        gas_price: int = 0
    ) -> Transaction:
        tx_type = TxType.SC_CALL
        sc_address_bytes: bytes
        if isinstance(sc_address, str):
            address_type = addr.check_name_address(sc_address)
            if address_type > 0:
                sc_address_bytes = sc_address.encode()
                if 2 == address_type:
                    tx_type = TxType.GOVERNANCE
            else:
                try:
                    sc_address_bytes = decode_address(sc_address)
                except Exception as e:
                    raise ValueError(
                        "Invalid smart contract address: {}".format(e))
        elif isinstance(sc_address, addr.GovernanceTxAddress):
            if addr.check_name_address(sc_address.value):
                sc_address_bytes = sc_address.value.encode()
                tx_type = TxType.GOVERNANCE
        else:
            sc_address_bytes = sc_address

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        call_info = CallInfo(func_name, args).__dict__
        payload = json.dumps(call_info, separators=(',', ':')).encode('utf-8')

        if nonce is None:
            if self.__account is None:
                raise GeneralException("Current account is not set")
            nonce = self.__account.nonce + 1

        return self.generate_tx(to_address=sc_address_bytes,
                                nonce=nonce, amount=amount,
                                gas_limit=gas_limit, gas_price=gas_price,
                                payload=payload, tx_type=tx_type)

    def batch_call_sc(
        self,
        sc_txs: List[Transaction]
    ) -> Tuple[List[Transaction], List[TxResult]]:
        return self.batch_tx(sc_txs)

    def call_sc(
        self,
        sc_address: Union[str, addr.GovernanceTxAddress, bytes],
        func_name: str,
        amount: int = 0,
        args: Optional[Any] = None,
        gas_limit: int = 0,
        gas_price: int = 0
    ) -> Tuple[Transaction, TxResult]:
        sc_tx = self.new_call_sc_tx(sc_address=sc_address, func_name=func_name,
                                    amount=amount, args=args,
                                    gas_limit=gas_limit, gas_price=gas_price)
        sc_txs, results = self.batch_call_sc([sc_tx])
        return sc_txs[0], results[0]

    def query_sc(
        self,
        sc_address: Union[bytes, str],
        func_name: str,
        args: Optional[Any] = None
    ):
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = addr.Address.decode(sc_address)

        if args is not None and not isinstance(args, (list, tuple)):
            args = [args]

        call_info = CallInfo(func_name, args).__dict__
        payload = json.dumps(call_info, separators=(',', ':')).encode('utf-8')

        try:
            result = self.__comm.query_contract(sc_address, payload)
        except Exception as e:
            raise CommunicationException(e) from e

        return result.value

    def query_sc_state(
        self,
        sc_address: Union[bytes, str],
        storage_keys: List[Union[bytes, str, SCStateVar]],
        root: bytes = b'',
        compressed: bool = True
    ) -> SCState:
        """ query_sc_state returns a SCState object containing the contract
        state and variable state with their respective merkle proofs.
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if isinstance(sc_address, str):
            # TODO exception handling: raise ValueError("Invalid checksum")
            sc_address = addr.Address.decode(sc_address)

        if isinstance(root, str) and len(root) != 0:
            root = decode_root(root)

        # convert SCStateVar objects to trie storage key strings
        trie_keys = []
        for key in storage_keys:
            if isinstance(key, bytes):
                trie_keys.append(hashlib.sha256(key).digest())
            elif isinstance(key, str):
                trie_keys.append(
                    hashlib.sha256(key.encode('latin-1')).digest())
            elif isinstance(key, SCStateVar):
                trie_keys.append(hashlib.sha256(bytes(key)).digest())
            else:
                assert False, ("Invalid key type provided, must be bytes, "
                               "str or SCStateVar")

        try:
            result = self.__comm.query_contract_state(sc_address, trie_keys,
                                                      root, compressed)
        except Exception as e:
            raise CommunicationException(e) from e

        account = acc.Account(empty=True)
        account.state = result.contractProof.state
        account.state_proof = result.contractProof
        account.address = sc_address  # type: ignore

        var_proofs = VarProofs(result.varProofs, trie_keys)

        return SCState(account=account, var_proofs=var_proofs)

    def get_conf_change_progress(self, block_height: int) -> ChangeConfInfo:
        """
        Returns the RAFT change config progress status after 'changeCluster'
        system contract
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            status = self.__comm.get_conf_change_progress(block_height)
        except Exception as e:
            raise CommunicationException(e) from e

        return ChangeConfInfo(status)

    def get_enterprise_config(self, key: str) -> EnterpriseConfig:
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        try:
            conf = self.__comm.get_enterprise_config(key)
        except Exception as e:
            raise CommunicationException(e) from e
        return EnterpriseConfig(conf)

    def get_name_info(self, name: str, block_height: int = -1):
        """
        Returns information of name which is designated by the system contract
        :param name:
        :param block_height:
        :return:
        """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")

        if block_height < 0:
            # set current block height
            block_height = self.get_status().best_block_height

        try:
            info = self.__comm.get_name_info(name, block_height)
        except Exception as e:
            raise CommunicationException(e) from e

        return NameInfo(info)

    def get_abi(self, contract_addr: str = None, addr_bytes: bytes = None):
        """ Returns the abi of given contract address. """
        if self.__comm is None:
            raise CommunicationException("Node connection not initialized")
        if contract_addr is not None:
            addr_bytes = decode_address(contract_addr)
        assert addr_bytes
        try:
            abi = self.__comm.get_abi(addr_bytes)
        except Exception as e:
            raise CommunicationException(e) from e
        return Abi(abi)

    def get_address(
        self,
        account: Optional[acc.Account] = None
    ) -> Optional[addr.Address]:
        if (account and isinstance(account, acc.Account)):
            return account.address
        if self.__account is None:
            raise GeneralException("Current account is not set")
        return self.__account.address

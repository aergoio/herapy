# -*- coding: utf-8 -*-

"""Communication(grpc) module."""

import grpc
from typing import (
    Optional,
    List
)

from .grpc import account_pb2, blockchain_pb2, rpc_pb2, rpc_pb2_grpc, raft_pb2
from .utils.converter import convert_tx_to_grpc_tx
from .obj.transaction import Transaction


class Comm:
    def __init__(
        self,
        target: Optional[str] = None,
        tls_ca_cert: Optional[bytes] = None,
        tls_cert: Optional[bytes] = None,
        tls_key: Optional[bytes] = None
    ):
        self.__target = target
        self.__tls_ca_cert = tls_ca_cert
        self.__tls_cert = tls_cert
        self.__tls_key = tls_key
        self.__channel = None
        self.__rpc_stub = None

    def connect(self):
        self.disconnect()

        if self.__tls_cert is not None:
            creds = grpc.ssl_channel_credentials(
                root_certificates=self.__tls_ca_cert,
                private_key=self.__tls_key, certificate_chain=self.__tls_cert
            )
            self.__channel = grpc.secure_channel(self.__target, creds)
        else:
            self.__channel = grpc.insecure_channel(self.__target)

        self.__rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(self.__channel)

    def disconnect(self):
        if self.__channel is not None:
            self.__channel.close()

    def create_account(self, address: bytes, passphrase: str):
        if self.__rpc_stub is None:
            return None
        account = account_pb2.Account(address=address)
        return self.__rpc_stub.CreateAccount(
            request=rpc_pb2.Personal(account=account, passphrase=passphrase)
        )

    def get_account_state(self, address: bytes):
        if self.__rpc_stub is None:
            return None

        rpc_account = account_pb2.Account()
        rpc_account.address = address
        return self.__rpc_stub.GetState(rpc_account)

    def get_account_state_proof(
        self,
        address: bytes,
        root: bytes,
        compressed: bool
    ):
        if self.__rpc_stub is None:
            return None
        account_and_root = rpc_pb2.AccountAndRoot(Account=address,
                                                  Root=root,
                                                  Compressed=compressed)
        return self.__rpc_stub.GetStateAndProof(account_and_root)

    def get_chain_info(self):
        if self.__rpc_stub is None:
            return None

        return self.__rpc_stub.GetChainInfo(rpc_pb2.Empty())

    def get_consensus_info(self):
        if self.__rpc_stub is None:
            return None

        return self.__rpc_stub.GetConsensusInfo(rpc_pb2.Empty())

    def get_node_info(self, keys: Optional[str]):
        if self.__rpc_stub is None:
            return None

        # currently not working
        key_params = rpc_pb2.KeyParams()
        if keys is not None:
            key_params.key.extend(keys)

        return self.__rpc_stub.GetServerInfo(key_params)

    def receive_event_stream(
        self,
        sc_address: bytes,
        event_name: str,
        start_block_no: int,
        end_block_no: int,
        with_desc: bool,
        arg_filter: Optional[bytes],
        recent_block_cnt: int
    ):
        if self.__rpc_stub is None:
            return None

        filter = blockchain_pb2.FilterInfo()
        filter.contractAddress = sc_address
        filter.eventName = event_name
        filter.blockfrom = start_block_no
        filter.blockto = end_block_no
        filter.desc = with_desc
        if arg_filter is not None:
            filter.argFilter = arg_filter
        filter.recentBlockCnt = recent_block_cnt

        return self.__rpc_stub.ListEventStream(filter)

    def get_events(
        self,
        sc_address: bytes,
        event_name: str,
        start_block_no: int,
        end_block_no: int,
        with_desc: bool,
        arg_filter: Optional[bytes],
        recent_block_cnt: int
    ):
        if self.__rpc_stub is None:
            return None

        filter = blockchain_pb2.FilterInfo()
        filter.contractAddress = sc_address
        filter.eventName = event_name
        if start_block_no > 0:
            filter.blockfrom = start_block_no
        if end_block_no > 0:
            filter.blockto = end_block_no
        filter.desc = with_desc
        if arg_filter is not None:
            filter.argFilter = arg_filter
        filter.recentBlockCnt = recent_block_cnt

        return self.__rpc_stub.ListEvents(filter)

    def receive_block_meta_stream(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.ListBlockMetadataStream(rpc_pb2.Empty())

    def receive_block_stream(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.ListBlockStream(rpc_pb2.Empty())

    def get_block_headers(
        self,
        block_hash: Optional[bytes],
        block_height: int,
        list_size: int,
        offset: int,
        is_asc_order: bool
    ):
        if self.__rpc_stub is None:
            return None
        params = rpc_pb2.ListParams()
        if block_hash is not None:
            params.hash = block_hash
        if block_height >= 0:
            params.height = block_height
        params.size = list_size
        params.offset = offset
        params.asc = is_asc_order
        return self.__rpc_stub.ListBlockHeaders(params)

    def get_block_metas(
        self,
        block_hash: Optional[bytes],
        block_height: int,
        list_size: int,
        offset: int,
        is_asc_order: bool
    ):
        if self.__rpc_stub is None:
            return None
        params = rpc_pb2.ListParams()
        if block_hash is not None:
            params.hash = block_hash
        if block_height >= 0:
            params.height = block_height
        params.size = list_size
        params.offset = offset
        params.asc = is_asc_order
        return self.__rpc_stub.ListBlockMetadata(params)

    def get_blockchain_status(self):
        if self.__rpc_stub is None:
            return None

        return self.__rpc_stub.Blockchain(rpc_pb2.Empty())

    def get_accounts(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.GetAccounts(rpc_pb2.Empty())

    def get_block(self, query: bytes):
        if self.__rpc_stub is None:
            return None
        v = rpc_pb2.SingleBytes()
        v.value = query
        return self.__rpc_stub.GetBlock(v)

    def get_block_meta(self, query: bytes):
        if self.__rpc_stub is None:
            return None
        v = rpc_pb2.SingleBytes()
        v.value = query
        return self.__rpc_stub.GetBlockMetadata(v)

    def get_peers(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.GetPeers(rpc_pb2.Empty())

    def get_node_state(self, timeout: int):
        if self.__rpc_stub is None:
            return None
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = timeout.to_bytes(8, byteorder='little')
        return self.__rpc_stub.NodeState(single_bytes)

    def get_tx(self, tx_hash: bytes):
        if self.__rpc_stub is None:
            return None
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        return self.__rpc_stub.GetTX(single_bytes)

    def get_block_tx(self, tx_hash: bytes):
        if self.__rpc_stub is None:
            return None
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        return self.__rpc_stub.GetBlockTX(single_bytes)

    def unlock_account(self, address: bytes, passphrase: str):
        if self.__rpc_stub is None:
            return None
        account = account_pb2.Account(address=address)
        personal = rpc_pb2.Personal(passphrase=passphrase, account=account)
        return self.__rpc_stub.UnlockAccount(request=personal)

    def lock_account(self, address: bytes, passphrase: str):
        if self.__rpc_stub is None:
            return None
        account = account_pb2.Account(address=address)
        personal = rpc_pb2.Personal(passphrase=passphrase, account=account)
        return self.__rpc_stub.LockAccount(request=personal)

    # This RPC is for making and sending Tx inside a node.
    # Don't use it for sending TX which is made by a client.
    def send_tx(self, unsigned_tx: Transaction):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.SendTX(convert_tx_to_grpc_tx(unsigned_tx))

    # This RPC is for sending signed Txs made by a client.
    def commit_txs(self, signed_txs: List[Transaction]):
        if self.__rpc_stub is None:
            return None
        rpc_txs = []
        for signed_tx in signed_txs:
            rpc_txs.append(convert_tx_to_grpc_tx(signed_tx))
        rpc_tx_list = blockchain_pb2.TxList()
        rpc_tx_list.txs.extend(rpc_txs)
        return self.__rpc_stub.CommitTX(rpc_tx_list)

    def get_receipt(self, tx_hash: bytes):
        if self.__rpc_stub is None:
            return None
        v = rpc_pb2.SingleBytes()
        v.value = tx_hash
        return self.__rpc_stub.GetReceipt(v)

    def query_contract(self, sc_address: bytes, query_info: bytes):
        query = blockchain_pb2.Query()
        if self.__rpc_stub is None:
            return None
        query.contractAddress = sc_address
        query.queryinfo = query_info
        return self.__rpc_stub.QueryContract(query)

    def query_contract_state(
        self,
        sc_address: bytes,
        storage_keys: List[bytes],
        root: bytes,
        compressed: bool
    ):
        if self.__rpc_stub is None:
            return None
        state_query = blockchain_pb2.StateQuery(contractAddress=sc_address,
                                                storageKeys=storage_keys,
                                                root=root,
                                                compressed=compressed)
        return self.__rpc_stub.QueryContractState(state_query)

    def get_conf_change_progress(self, block_height: int):
        if self.__rpc_stub is None:
            return None

        v = rpc_pb2.SingleBytes()
        v.value = block_height.to_bytes(8, byteorder='little')
        return self.__rpc_stub.GetConfChangeProgress(v)

    def get_enterprise_config(self, key: str):
        if self.__rpc_stub is None:
            return None

        v = rpc_pb2.EnterpriseConfigKey()
        v.key = key
        return self.__rpc_stub.GetEnterpriseConfig(v)

    def get_name_info(self, name: str, block_height: int):
        if self.__rpc_stub is None:
            return None

        n = rpc_pb2.Name()
        n.name = name
        n.blockNo = block_height
        return self.__rpc_stub.GetNameInfo(n)

    def get_abi(self, addr_bytes: bytes):
        if self.__rpc_stub is None:
            return None
        v = rpc_pb2.SingleBytes()
        v.value = addr_bytes
        return self.__rpc_stub.GetABI(v)

    def add_raft_member(
        self,
        request_id: int,
        member_id: int,
        member_name: str,
        member_address: str,
        member_peer_id: bytes
    ):
        if self.__rpc_stub is None:
            return None
        ch = raft_pb2.MembershipChange()
        ch.type = raft_pb2.ADD_MEMBER
        ch.requestID = request_id
        ch.attr = raft_pb2.MemberAttr()
        ch.attr.ID = member_id
        ch.attr.name = member_name
        ch.attr.address = member_address
        ch.attr.peerID = member_peer_id
        return self.__rpc_stub.ChangeMembership(ch)

    def del_raft_member(
        self,
        request_id: int,
        member_id: int,
        member_name: str,
        member_address: str,
        member_peer_id: bytes
    ):
        if self.__rpc_stub is None:
            return None
        ch = raft_pb2.MembershipChange()
        ch.type = raft_pb2.REMOVE_MEMBER
        ch.requestID = request_id
        ch.attr = raft_pb2.MemberAttr()
        ch.attr.ID = member_id
        ch.attr.name = member_name
        ch.attr.address = member_address
        ch.attr.peerID = member_peer_id
        return self.__rpc_stub.ChangeMembership(ch)

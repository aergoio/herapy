# -*- coding: utf-8 -*-

import json
import enum

from .aer import Aer
from .block_hash import BlockHash
from .event import Event
from .tx_hash import TxHash
from ..status.commit_status import CommitStatus
from ..status.tx_result_status import TxResultStatus
from ..grpc.rpc_pb2 import CommitResult
from ..grpc.blockchain_pb2 import Receipt
from ..utils.encoding import encode_tx_hash, encode_address, encode_b58


@enum.unique
class TxResultType(enum.Enum):
    COMMIT_RESULT = 0
    RECEIPT = 1


class TxResult:
    def __init__(self, result, tx=None):
        self.tx = tx
        self.__result = result

        if type(result) == Receipt:
            self.__type = TxResultType.RECEIPT
            try:
                self.status = TxResultStatus(result.status)
                self.detail = result.ret
            except:
                self.status = TxResultStatus.ERROR
                self.detail = result.status
            self.contract_address = encode_address(result.contractAddress)
            self.fee_used = Aer(result.feeUsed)
            self.cumulative_fee_used = Aer(result.cumulativeFeeUsed)
            self.bloom = result.bloom
            self.event_list = []
            for e in result.events:
                self.event_list.append(Event(e))
            self.block_no = result.blockNo
            self.block_hash = BlockHash(result.blockHash)
            self.tx_index = result.txIndex
            self.tx_hash = TxHash(result.txHash)
            self.from_address = encode_address(getattr(result, 'from'))
            self.to_address = encode_address(result.to)

            """
            if result.ret is None or 0 == len(result.ret):
                self.status = TxResultStatus.ERROR
                if 'CREATED' != result.status:
                    self.detail = result.status
            """
        elif type(result) == CommitResult:
            self.__type = TxResultType.COMMIT_RESULT
            self.tx_id = encode_tx_hash(self.__result.hash)
            self.status = CommitStatus(self.__result.error)
            self.detail = self.__result.detail
            self.contract_address = None
            self.fee_used = None
            self.cumulative_fee_used = None
            self.bloom = None
            self.event_list = []
            self.block_no = -1
            self.block_hash = None
            self.tx_index = -1
            self.tx_hash = None
            self.from_address = None
            self.to_address = None

    @property
    def type(self):
        return self.__type

    def json(self):
        return {
            'type': self.__type.name,
            'tx_id': self.tx_id,
            'status': self.status.name,
            'detail': self.detail,
            'contract_address': self.contract_address,
            'fee_used': str(self.fee_used) if self.fee_used is not None else None,
            'cumulative_fee_used': str(self.cumulative_fee_used) if self.cumulative_fee_used is not None else None,
            'bloom': encode_b58(self.bloom) if self.bloom is not None else None,
            'event_list': self.event_list,
            'block_no': self.block_no,
            'block_hash': str(self.block_hash) if self.block_hash is not None else None,
            'tx_index': self.tx_index,
            'tx_hash': str(self.tx_hash) if self.tx_hash is not None else None,
            'from_address': self.from_address,
            'to_address': self.to_address,
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)

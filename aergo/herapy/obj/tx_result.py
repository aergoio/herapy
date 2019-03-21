# -*- coding: utf-8 -*-

import json
import enum

from ..utils.encoding import encode_tx_hash, encode_address
from ..grpc.rpc_pb2 import CommitResult
from ..status.commit_status import CommitStatus
from ..status.tx_result_status import TxResultStatus
from ..grpc.blockchain_pb2 import Receipt


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

    @property
    def type(self):
        return self.__type

    def __str__(self):
        result = {
            'tx_id': self.tx_id,
            'status': self.status.name,
            'detail': self.detail,
            'contract_address': self.contract_address
        }
        return json.dumps(result, indent=2)

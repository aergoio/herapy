# -*- coding: utf-8 -*-

import json

from ..utils.encoding import encode_tx_hash, encode_address
from ..grpc.rpc_pb2 import CommitResult
from ..status.commit_status import CommitStatus
from ..status.tx_result_status import TxResultStatus
from ..grpc.blockchain_pb2 import Receipt


class TxResult:
    def __init__(self, result, tx=None):
        self.tx = tx
        self.__result = result

        if type(result) == Receipt:
            self.status = TxResultStatus(self.__result.status)
            self.detail = result.ret
            self.contract_address = encode_address(result.contractAddress)

            if 'error' in result.ret:
                self.status = TxResultStatus.ERROR
                if 'CREATED' != result.status:
                    self.detail = result.status
        elif type(result) == CommitResult:
            self.tx_id = encode_tx_hash(self.__result.hash)
            self.status = CommitStatus(self.__result.error)
            self.detail = self.__result.detail
            self.contract_address = None

    def __str__(self):
        result = {
            'tx_id': self.tx_id,
            'status': self.status.name,
            'detail': self.detail,
            'contract_address': self.contract_address
        }
        return json.dumps(result, indent=2)

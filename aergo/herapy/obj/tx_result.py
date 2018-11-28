# -*- coding: utf-8 -*-

import json

from ..utils.encoding import encode_tx_hash
from ..status.commit_status import CommitStatus


class TxResult:
    def __init__(self, tx=None, result=None):
        self.tx = tx
        self.__result = result

        if result is not None:
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

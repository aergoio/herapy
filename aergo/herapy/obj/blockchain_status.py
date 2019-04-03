# -*- coding: utf-8 -*-

import json

from .block_hash import BlockHash
from .consensus_info import ConsensusInfo
from ..utils.encoding import encode_b58


class BlockchainStatus:
    def __init__(self, status):
        self._status = status
        self._bbh = BlockHash(self._status.best_block_hash)
        self._consensus_info = ConsensusInfo(self._status.consensus_info)

    @property
    def best_block_hash(self):
        return self._bbh

    @property
    def best_block_height(self):
        return self._status.best_height

    @property
    def best_chain_id_hash(self):
        return self._status.best_chain_id_hash

    @property
    def best_chain_id_hash_b58(self):
        return encode_b58(self._status.best_chain_id_hash)

    @property
    def consensus_info(self):
        return self._consensus_info

    def json(self):
        return {
            "best_block_hash": str(self.best_block_hash),
            "best_block_height": self.best_block_height,
            "best_chain_id_hash": self.best_chain_id_hash_b58,
            "consensus_info": self.consensus_info.json(),
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)
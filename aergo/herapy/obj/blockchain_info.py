# -*- coding: utf-8 -*-

import json

from .aer import Aer
from .chain_id import ChainID
from .consensus_info import ConsensusInfo


class BlockchainInfo:
    def __init__(self, chain_info, consensus_info=None):
        self._chain_info = chain_info
        self._chain_id = ChainID(self._chain_info.id)
        if consensus_info is not None:
            self._consensus_info = ConsensusInfo(consensus_info)
        else:
            self._consensus_info = ConsensusInfo(None,
                                                 self._chain_id.consensus)

    @property
    def number_of_bp(self):
        return self._chain_info.bpNumber

    @property
    def max_block_size(self):
        return self._chain_info.maxblocksize

    @property
    def max_tokens(self):
        return Aer(self._chain_info.maxtokens)

    @property
    def minimum_staking(self):
        return Aer(self._chain_info.stakingminimum)

    @property
    def total_staking(self):
        return Aer(self._chain_info.totalstaking)

    @property
    def gas_price(self):
        return Aer(self._chain_info.gasprice)

    @property
    def name_price(self):
        return Aer(self._chain_info.nameprice)

    @property
    def consensus_info(self):
        return self._consensus_info

    def json(self):
        return {
            "chain_id": self._chain_id.json(),
            "number_of_bp": str(self.number_of_bp),
            "max_block_size": self.max_block_size,
            "max_tokens": str(self.max_tokens),
            "minimum_staking": str(self.minimum_staking),
            "total_staking": str(self.total_staking),
            "gas_price": str(self.gas_price),
            "name_price": str(self.name_price),
            "consensus_info": self._consensus_info.json(),
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)
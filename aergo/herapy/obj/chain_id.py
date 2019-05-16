# -*- coding: utf-8 -*-

import json


class ChainID:
    def __init__(self, chain_id):
        self._chain_id = chain_id

    @property
    def magic(self):
        return self._chain_id.magic

    @property
    def is_public(self):
        return self._chain_id.public

    @property
    def is_mainnet(self):
        return self._chain_id.mainnet

    @property
    def consensus(self):
        return self._chain_id.consensus

    def json(self):
        return {
            'magic': self.magic,
            'is_public': self.is_public,
            'is_mainnet': self.is_mainnet,
            'consensus': self.consensus,
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)


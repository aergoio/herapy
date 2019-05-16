# -*- coding: utf-8 -*-

import json

from .block_hash import BlockHash
from .peer import Peer
from ..grpc.rpc_pb2 import ConsensusInfo as CInfo


def _get_dict_value(d, k):
    if d is None:
        return None

    if k in d:
        return d[k]
    else:
        return None


class ConsensusInfo:
    def __init__(self, info, consensus_type=None):
        if isinstance(info, str):
            info = json.loads(info)
            self._info = info
            self._type = _get_dict_value(info, 'Type')
            self._status = _get_dict_value(info, 'Status')
            lib_hash = _get_dict_value(info, 'LibHash')
            if lib_hash is not None:
                self._lib_hash = BlockHash(lib_hash)
            else:
                self._lib_hash = None
            self._lib_no = _get_dict_value(info, 'LibNo')
            self._block_producer_list = []
        elif type(info) == CInfo:
            self._info = info
            self._type = info.type
            self._status = None
            self._lib_hash = None
            self._lib_no = None
            self._block_producer_list = []
            for bp in info.bps:
                self._block_producer_list.append(json.loads(bp))
        elif consensus_type:
            self._info = None
            self._type = consensus_type
            self._status = None
            self._lib_hash = None
            self._lib_no = None
            self._block_producer_list = []
        else:
            raise ValueError("Cannot recognize the value: {}".format(info))

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @property
    def lib_hash(self):
        """
        get the last irreversible block (LIB) hash
        :return:
        """
        return self._lib_hash

    @property
    def lib_no(self):
        """
        get the last irreversible block (LIB) number
        :return:
        """
        return self._lib_no

    @property
    def block_producer_list(self):
        return self._block_producer_list

    def json(self):
        return {
            'type': self.type,
            'status': self.status,
            'lib_hash': self.lib_hash,
            'lib_no': self.lib_no,
            'block_producer_list': self.block_producer_list,
        }

    def __str__(self):
        return json.dumps(self.json(), indent=2)


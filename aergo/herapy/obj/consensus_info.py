# -*- coding: utf-8 -*-

import json

from .block_hash import BlockHash


class ConsensusInfo:
    def __init__(self, info):
        if isinstance(info, str):
            info = json.loads(info)
        self._info = info

    @property
    def type(self):
        if 'Type' in self._info:
            return self._info['Type']
        else:
            return None

    @property
    def status(self):
        if 'Status' in self._info:
            return self._info['Status']
        else:
            return None

    @property
    def lib_hash(self):
        """
        get the last irreversible block (LIB) hash
        :return:
        """
        status = self.status
        if status is not None:
            if 'LibHash' in self._info:
                return BlockHash(self._info['LibHash'])
            else:
                return None

    @property
    def lib_no(self):
        """
        get the last irreversible block (LIB) number
        :return:
        """
        status = self.status
        if status is not None:
            if 'LibNo' in self._info:
                return self._info['LibNo']
            else:
                return None

    def __str__(self):
        return json.dumps(self._info, indent=2)


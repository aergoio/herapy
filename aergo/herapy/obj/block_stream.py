# -*- coding: utf-8 -*-

from .stream import Stream
from .block import Block


class BlockStream(Stream):
    def __init__(self, block_stream):
        super().__init__(block_stream)

    def next(self):
        return Block(grpc_block=next(self._grpc_stream))

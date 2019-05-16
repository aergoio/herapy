# -*- coding: utf-8 -*-

from .stream import Stream
from .block import Block


class BlockMetaStream(Stream):
    def __init__(self, block_meta_stream):
        super().__init__(block_meta_stream)

    def __next__(self):
        grpc_block_meta = next(self._grpc_stream)
        return Block(hash_value=grpc_block_meta.hash,
                     grpc_block_header=grpc_block_meta.header,
                     tx_cnt=grpc_block_meta.txcount)


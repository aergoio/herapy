# -*- coding: utf-8 -*-

from typing import Union
from ..utils.encoding import encode_block_hash, decode_block_hash


class BlockHash:
    def __init__(self, bh: Union[str, bytes]) -> None:
        if isinstance(bh, str):
            hash_bytes = decode_block_hash(bh)
            assert hash_bytes  # for mypy Optional[bytes] -> bytes
            bh = hash_bytes
        self.__block_hash = bh

    @property
    def value(self) -> bytes:
        return self.__block_hash

    def __bytes__(self) -> bytes:
        return self.__block_hash

    def __str__(self) -> str:
        hash_str = encode_block_hash(self.__block_hash)
        assert hash_str
        return hash_str

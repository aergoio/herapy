# -*- coding: utf-8 -*-

from typing import Optional
from ..utils.encoding import encode_tx_hash


class TxHash:
    def __init__(self, th: Optional[bytes]) -> None:
        self.__tx_hash = th

    def __str__(self) -> str:
        hash_str = encode_tx_hash(self.__tx_hash)
        return '' if hash_str is None else hash_str

    def __bytes__(self) -> bytes:
        return self.__tx_hash if self.__tx_hash else b''

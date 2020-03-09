# -*- coding: utf-8 -*-

import ecdsa
import enum
from typing import (
    Union,
    Optional
)

from ..utils.encoding import encode_address, decode_address
from ..utils.converter import convert_bytes_to_public_key, \
    convert_public_key_to_bytes


MAX_NAME_ADDRESS_LEN = 12


@enum.unique
class GovernanceTxAddress(enum.Enum):
    SYSTEM = "aergo.system"
    NAME = "aergo.name"
    ENTERPRISE = "aergo.enterprise"


def check_name_address(addr: str) -> int:
    if len(addr) <= MAX_NAME_ADDRESS_LEN:
        return 1
    elif addr in set(e.value for e in GovernanceTxAddress):
        return 2
    else:
        return 0


class Address:
    def __init__(
        self,
        pubkey: Union[str, bytes, ecdsa.ecdsa.Public_key],
        empty: bool = False,
        curve: ecdsa.curves.Curve = ecdsa.SECP256k1
    ) -> None:
        self.__address = None
        self.__curve = curve
        self.__empty = empty

        if empty:
            return

        if pubkey is None:
            assert 1 == 0

        if isinstance(pubkey, str):
            pubkey = decode_address(pubkey)
        elif isinstance(pubkey, bytes):
            pubkey = convert_bytes_to_public_key(pubkey, curve=curve)

        self.__address = convert_public_key_to_bytes(
            pubkey=pubkey, curve=curve, compressed=True)

    def __str__(self) -> str:
        return self.encode(self.__address)

    def __bytes__(self) -> bytes:
        if self.__address is None:
            return b''
        return self.__address

    @property
    def value(self) -> Optional[bytes]:
        return self.__address

    @value.setter
    def value(self, v: Union[str, bytes]) -> None:
        if self.__empty:
            if isinstance(v, str):
                self.__address = self.decode(v)
            elif isinstance(v, bytes):
                self.__address = v
        else:
            raise ValueError('Cannot set a value for the derived address')

    @property
    def curve(self) -> ecdsa.curves.Curve:
        return self.__curve

    @property
    def public_key(self) -> Optional[ecdsa.ecdsa.Public_key]:
        return None if self.__address is None else \
            convert_bytes_to_public_key(self.__address, curve=self.__curve)

    @staticmethod
    def encode(addr: Optional[bytes]) -> str:
        try:
            if addr is None or 0 == len(addr):
                return ''
            elif len(addr) < 32:
                return str(addr, 'UTF-8')
        except:
            pass
        assert addr
        return encode_address(addr)

    @staticmethod
    def decode(addr: Optional[str]) -> bytes:
        try:
            if addr is None or 0 == len(addr):
                return b''
            elif check_name_address(addr) > 0:
                return addr.encode()
        except:
            pass

        assert addr
        return decode_address(addr)

import pytest

import ecdsa
import hashlib

from aergo.herapy.obj.address import Address
from aergo.herapy.utils.encoding import decode_address
from aergo.herapy.utils.converter import convert_public_key_to_bytes


def test_fail():
    with pytest.raises(AssertionError):
        Address(None)

    with pytest.raises(TypeError):
        Address(1234)

    with pytest.raises(ValueError):
        Address("1234")

    with pytest.raises(TypeError):
        Address(["1234"])


def test_success():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                   hashfunc=hashlib.sha256)
    addr = Address(pubkey=sk.privkey.public_key)
    assert type(addr) is Address
    assert isinstance(str(addr), str)
    assert isinstance(bytes(addr), bytes)
    assert bytes(addr) == convert_public_key_to_bytes(pubkey=addr.public_key,
                                                      curve=addr.curve,
                                                      compressed=True)
    with pytest.raises(ValueError):
        addr.value = str(addr)

    addr_str = str(addr)

    addr2 = Address(None, empty=True)
    addr2.value = addr_str
    assert type(addr2) is Address
    assert isinstance(str(addr2), str)
    assert isinstance(bytes(addr2), bytes)
    assert bytes(addr2) == convert_public_key_to_bytes(pubkey=addr2.public_key,
                                                       curve=addr2.curve,
                                                       compressed=True)

    assert str(addr2) == str(addr)
    assert bytes(addr2) == bytes(addr)
    assert addr2.public_key.point == addr.public_key.point
    assert convert_public_key_to_bytes(pubkey=addr.public_key,
                                       curve=addr.curve,
                                       compressed=False) == \
           convert_public_key_to_bytes(pubkey=addr2.public_key,
                                       curve=addr2.curve,
                                       compressed=False)

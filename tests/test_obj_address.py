import pytest

import ecdsa
import hashlib

from aergo.herapy.obj.address import Address
from aergo.herapy.utils.encoding import decode_address


def test_fail():
    with pytest.raises(AssertionError):
        Address(None)

    with pytest.raises(TypeError):
        Address(pubkey=1234)

    with pytest.raises(TypeError):
        Address(address=1234)

    with pytest.raises(ValueError):
        Address(pubkey="1234")

    with pytest.raises(ValueError):
        Address(address="1234")

    with pytest.raises(ValueError):
        Address(pubkey=["1234"])

    with pytest.raises(TypeError):
        Address(address=["1234"])


def test_success():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                   hashfunc=hashlib.sha256)
    addr = Address(pubkey=sk.privkey.public_key)
    assert type(addr) is Address
    assert isinstance(str(addr), str)
    assert isinstance(bytes(addr), bytes)
    assert decode_address(str(addr)) == addr.get_public_key()

    addr_str = str(addr)

    addr2 = Address(address=addr_str)
    assert type(addr2) is Address
    assert isinstance(str(addr2), str)
    assert str(addr2) == str(addr)
    assert addr.get_public_key() == addr2.get_public_key()
    assert addr.get_public_key(compressed=False) == addr2.get_public_key(compressed=False)

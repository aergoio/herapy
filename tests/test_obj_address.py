import pytest

import ecdsa
import hashlib

from aergo.herapy.obj.address import Address


def test_fail():
    with pytest.raises(AssertionError):
        Address(None)

    with pytest.raises(AttributeError):
        Address(1234)

    with pytest.raises(ValueError):
        Address("1234")


def test_success():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                   hashfunc=hashlib.sha256)
    addr = Address(sk.privkey.public_key)
    assert type(addr) is Address
    assert isinstance(str(addr), str)
    assert isinstance(bytes(addr), bytes)

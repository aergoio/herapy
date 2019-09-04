import pytest

import ecdsa
import hashlib

from aergo.herapy.obj.address import Address
from aergo.herapy.utils.encoding import encode_address, decode_address
from aergo.herapy.utils.converter import convert_public_key_to_bytes


def test_error():
    with pytest.raises(AssertionError):
        Address(pubkey=None)

    with pytest.raises(TypeError):
        Address(pubkey=1234)

    with pytest.raises(ValueError):
        Address(pubkey="1234")

    with pytest.raises(TypeError):
        Address(pubkey=["1234"])


def test_success():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1,
                                   hashfunc=hashlib.sha256)
    addr = Address(pubkey=sk.privkey.public_key)
    assert type(addr) is Address
    assert isinstance(str(addr), str)
    assert isinstance(bytes(addr), bytes)
    assert bytes(addr) == addr.value
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
    assert bytes(addr2) == addr2.value
    assert bytes(addr2) == convert_public_key_to_bytes(pubkey=addr2.public_key,
                                                       curve=addr2.curve,
                                                       compressed=True)

    assert addr2 != addr
    assert addr2.value == addr.value
    assert str(addr2) == str(addr)
    assert bytes(addr2) == bytes(addr)
    assert addr2.public_key.point == addr.public_key.point
    assert convert_public_key_to_bytes(pubkey=addr.public_key,
                                       curve=addr.curve,
                                       compressed=False) == \
           convert_public_key_to_bytes(pubkey=addr2.public_key,
                                       curve=addr2.curve,
                                       compressed=False)

    pubkey3 = convert_public_key_to_bytes(pubkey=addr.public_key,
                                          curve=addr.curve,
                                          compressed=False)
    pubkey4 = convert_public_key_to_bytes(pubkey=addr2.public_key,
                                          curve=addr.curve,
                                          compressed=True)
    addr3 = Address(pubkey=pubkey3)
    assert addr3.value == addr.value
    assert bytes(addr3) == bytes(addr)
    addr4 = Address(pubkey=pubkey4)
    assert addr4.value == addr2.value
    assert bytes(addr4) == bytes(addr2)

    assert addr4 != addr3
    assert str(addr4) == str(addr3)
    assert bytes(addr4) == bytes(addr3)
    assert addr4.public_key.point == addr3.public_key.point

    addr5 = Address(None, empty=True)
    addr5.value = bytes(addr3)
    assert addr4 != addr5
    assert str(addr4) == str(addr5)
    assert bytes(addr4) == bytes(addr5)
    assert addr4.public_key.point == addr5.public_key.point


def test_encode_empty():
    addr = Address(None, empty=True)
    assert str(addr) == ''

    addr = Address(None, empty=True)
    addr.value = bytes([])
    assert str(addr) == ''


def test_govname():
    addr = Address(None, empty=True)
    name = 'abcdetest'
    addr.value = name.encode()
    assert len(str(addr)) == len(name)

    addr = Address(None, empty=True)
    baddr = bytes([0x61, 0x65, 0x72, 0x67, 0x6f, 0x2e, 0x65, 0x6e, 0x74, 0x65, 0x72, 0x70, 0x72, 0x69, 0x73, 0x65])
    addr.value = baddr
    assert str(addr) == 'aergo.enterprise'
    assert str(addr) == Address.encode(baddr)
    assert bytes(addr) == Address.decode('aergo.enterprise')
    assert baddr == Address.decode('aergo.enterprise')

    addr = Address(None, empty=True)
    addr.value = 'aergo.system'
    assert str(addr) == 'aergo.system'
    assert bytes(addr) == Address.decode('aergo.system')

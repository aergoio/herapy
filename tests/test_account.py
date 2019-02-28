import pytest

import ecdsa
import hashlib

from aergo.herapy.utils.encoding import decode_private_key
from aergo.herapy.utils.converter import convert_public_key_to_bytes
from aergo.herapy.account import Account
from aergo.herapy.obj.private_key import PrivateKey
from aergo.herapy.obj.address import Address


def test_import():
    # exported key from aergocli with password 1234
    # private key: 6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb
    # address: AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa
    exported_key = "47Nn73DSkBjHSfxvkJtiR3PACzQEZUN8qbjT41fYUfVEYipRZPwY4TnNRz5ahFHgN5naoJfJz"
    exported_key = decode_private_key(exported_key)

    acc = Account.decrypt_account(exported_key, '1234')
    assert str(acc.address) == "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"
    assert str(acc.private_key) == "6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb"

    assert acc.address == acc.private_key.address
    assert acc.public_key == acc.private_key.public_key
    assert acc.public_key.point == acc.private_key.public_key.point
    assert acc.public_key != acc.address.public_key
    assert acc.public_key.point == acc.address.public_key.point
    assert acc.private_key.public_key != acc.address.public_key
    assert acc.private_key.public_key.point == acc.address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(acc.public_key)
    assert bytes(acc.address) == convert_public_key_to_bytes(acc.private_key.public_key)
    assert bytes(acc.address) == convert_public_key_to_bytes(acc.address.public_key)
    assert bytes(acc.private_key.address) == convert_public_key_to_bytes(acc.public_key)

    private_key = PrivateKey(pk="6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb")
    assert acc.public_key != private_key.public_key
    assert acc.public_key.point == private_key.public_key.point
    assert private_key.public_key != acc.address.public_key
    assert private_key.public_key.point == acc.address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(private_key.public_key)
    assert bytes(private_key.address) == convert_public_key_to_bytes(acc.public_key)

    address = Address(None, empty=True)
    address.value = "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"
    assert acc.address != address
    assert bytes(acc.address) == bytes(address)
    assert private_key.address != address
    assert bytes(private_key.address) == bytes(address)

    assert acc.public_key != address.public_key
    assert acc.public_key.point == address.public_key.point
    assert private_key.public_key != address.public_key
    assert private_key.public_key.point == address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(address.public_key)
    assert bytes(private_key.address) == convert_public_key_to_bytes(address.public_key)

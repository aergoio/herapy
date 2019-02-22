import pytest

import ecdsa
import hashlib

from aergo.herapy.utils.encoding import decode_private_key
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
    assert acc.public_key == acc.address.public_key

    assert acc.get_public_key(True) == acc.address.get_public_key(True)
    assert acc.get_public_key(True) == acc.private_key.get_public_key(True)
    assert acc.get_public_key(False) == acc.address.get_public_key(False)
    assert acc.get_public_key(False) == acc.private_key.get_public_key(False)
    assert acc.private_key.get_public_key(True) == acc.private_key.address.get_public_key(True)
    assert acc.private_key.get_public_key(False) == acc.private_key.address.get_public_key(False)

    private_key = PrivateKey(pk="6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb")
    assert acc.public_key != private_key.public_key
    assert acc.get_public_key(True) == private_key.get_public_key(True)
    assert acc.get_public_key(False) == private_key.get_public_key(False)
    assert acc.get_public_key(True) == private_key.address.get_public_key(True)
    assert acc.get_public_key(False) == private_key.address.get_public_key(False)

    address = Address(pubkey=None, address="AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa")
    assert acc.public_key != address.public_key
    assert private_key.public_key != address.public_key
    assert acc.get_public_key(True) == address.get_public_key(True)
    assert acc.get_public_key(False) == address.get_public_key(False)
    assert private_key.get_public_key(True) == address.get_public_key(True)
    assert private_key.get_public_key(False) == address.get_public_key(False)
    assert private_key.address.get_public_key(True) == address.get_public_key(True)
    assert private_key.address.get_public_key(False) == address.get_public_key(False)

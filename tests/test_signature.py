import hashlib
import pytest

from aergo.herapy.obj.private_key import PrivateKey
from aergo.herapy.obj.address import Address
from aergo.herapy.utils.signature import verify_sig


def test_signature():
    msg = bytes("test", 'utf-8')
    h = hashlib.sha256(msg).digest()
    priv_key = PrivateKey(None)
    signature = priv_key.sign_msg(h)
    address = Address(priv_key.public_key).__str__()

    # check success
    assert verify_sig(h, signature, address)

    # check wrong signature from another key
    priv_key = PrivateKey(None)
    signature = priv_key.sign_msg(h)
    assert not verify_sig(h, signature, address)

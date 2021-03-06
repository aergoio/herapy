import pytest

from ecdsa.ecdsa import Public_key

from aergo.herapy.obj.private_key import PrivateKey
from aergo.herapy.utils.encoding import decode_private_key

PK_STR = "6jEuQyF6RZ9xpk7s99LzHoY2X7MeT8V88HCrsewwmynbKXtwUxZ"


def test_fail() -> None:
    with pytest.raises(TypeError):
        PrivateKey()  # type: ignore

    with pytest.raises(TypeError):
        PrivateKey(1234)  # type: ignore

    with pytest.raises(ValueError):
        PrivateKey("1234")


def test_success() -> None:
    # generate new private key
    pk = PrivateKey(None)
    assert type(pk) is PrivateKey
    assert isinstance(str(pk), str)
    assert isinstance(bytes(pk), bytes)
    assert type(pk.public_key) is Public_key

    # from private string
    pk = PrivateKey(PK_STR)
    assert type(pk) is PrivateKey
    assert isinstance(str(pk), str)
    assert PK_STR == str(pk)
    assert isinstance(bytes(pk), bytes)
    assert decode_private_key(PK_STR) == bytes(pk)
    assert type(pk.public_key) is Public_key

    # from private bytes
    pk = PrivateKey(decode_private_key(PK_STR))
    assert type(pk) is PrivateKey
    assert isinstance(str(pk), str)
    assert PK_STR == str(pk)
    assert isinstance(bytes(pk), bytes)
    assert decode_private_key(PK_STR) == bytes(pk)
    assert type(pk.public_key) is Public_key


def test_sign() -> None:
    msg = "test"
    msg_bytes = msg.encode('utf-8')

    pk = PrivateKey(None)
    with pytest.raises(TypeError):
        pk.sign_msg(msg)  # type: ignore
    sign = pk.sign_msg(msg_bytes)
    assert isinstance(sign, bytes)
    with pytest.raises(TypeError):
        pk.verify_sign(msg, sign)  # type: ignore
    assert pk.verify_sign(msg_bytes, sign)
    assert not pk.verify_sign("test1".encode('utf-8'), sign)
    with pytest.raises(TypeError):
        pk.verify_sign(msg_bytes, b'\x10')
    with pytest.raises(IndexError):
        pk.verify_sign(msg_bytes, b'\x30')
    with pytest.raises(TypeError):
        pk.verify_sign(msg_bytes, b'\x30\x02')
    with pytest.raises(TypeError):
        pk.verify_sign(msg_bytes, b'\x30\x04\x00\x00\x00\x00')
    with pytest.raises(TypeError):
        pk.verify_sign(msg_bytes, b'\x30\x04\x02\x00\x00\x00')
    with pytest.raises(ValueError):
        pk.verify_sign(msg_bytes, b'\x30\x04\x02\x00\x02\x00')


def test_asym_sec_msg() -> None:
    msg = "asymmetric encrypt/decrypt test"

    pk1 = PrivateKey(None)
    pk2 = PrivateKey(None)

    enc_msg = pk1.asymmetric_encrypt_msg(pk2.address, msg)
    dec_msg = pk2.asymmetric_decrypt_msg(pk1.address, enc_msg)

    assert msg == str(dec_msg, encoding='utf-8')

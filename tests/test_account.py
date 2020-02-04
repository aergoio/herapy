import pytest

import ecdsa
import hashlib

from aergo.herapy.utils.encoding import decode_private_key, encode_b64, \
    encode_address, encode_b58
from aergo.herapy.utils.converter import convert_public_key_to_bytes, \
    bytes_to_int_str
from aergo.herapy.account import Account
from aergo.herapy.obj.private_key import PrivateKey
from aergo.herapy.obj.address import Address


# exported key from aergocli with password 1234
# private key: 6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb
# address: AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa
exported_key_str = "47Nn73DSkBjHSfxvkJtiR3PACzQEZUN8qbjT41fYUfVEYipRZPwY4TnNRz5ahFHgN5naoJfJz"
exported_key = decode_private_key(exported_key_str)


def test_import():
    acc = Account.decrypt_account(exported_key, '1234')
    assert str(acc.address) == "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"
    assert str(acc.private_key) == "6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb"

    assert acc.address == acc.private_key.address
    assert acc.public_key == acc.private_key.public_key
    assert acc.public_key.point == acc.private_key.public_key.point
    assert acc.public_key == acc.address.public_key
    assert acc.public_key.point == acc.address.public_key.point
    assert acc.private_key.public_key == acc.address.public_key
    assert acc.private_key.public_key.point == acc.address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(acc.public_key)
    assert bytes(acc.address) == convert_public_key_to_bytes(acc.private_key.public_key)
    assert bytes(acc.address) == convert_public_key_to_bytes(acc.address.public_key)
    assert bytes(acc.private_key.address) == convert_public_key_to_bytes(acc.public_key)

    private_key = PrivateKey(pk="6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb")
    assert acc.public_key == private_key.public_key
    assert acc.public_key.point == private_key.public_key.point
    assert private_key.public_key == acc.address.public_key
    assert private_key.public_key.point == acc.address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(private_key.public_key)
    assert bytes(private_key.address) == convert_public_key_to_bytes(acc.public_key)

    address = Address(None, empty=True)
    address.value = "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"
    assert acc.address != address
    assert bytes(acc.address) == bytes(address)
    assert private_key.address != address
    assert bytes(private_key.address) == bytes(address)

    assert acc.public_key == address.public_key
    assert acc.public_key.point == address.public_key.point
    assert private_key.public_key == address.public_key
    assert private_key.public_key.point == address.public_key.point

    assert bytes(acc.address) == convert_public_key_to_bytes(address.public_key)
    assert bytes(private_key.address) == convert_public_key_to_bytes(address.public_key)


def test_keys():
    acc = Account.decrypt_account(exported_key, '1234')
    assert str(acc.address) == "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"

    signing_key = acc.private_key.get_signing_key()
    verifying_key = signing_key.get_verifying_key()
    print("to pem = {}".format(verifying_key.to_pem()))
    print("int(private key bytes) = {}".format(bytes_to_int_str(bytes(acc.private_key))))

    pubkey_bytes = convert_public_key_to_bytes(acc.public_key)
    print("compressed bytes(public key) = {}".format(pubkey_bytes))
    print("compressed int(public key bytes) = {}".format(bytes_to_int_str(pubkey_bytes)))

    address = encode_address(pubkey_bytes)
    print("compressed address = {}".format(address))
    assert address == str(acc.address)

    nocomp_pubkey_bytes = convert_public_key_to_bytes(acc.public_key, compressed=False)
    print("no compressed bytes(public key) = {}".format(pubkey_bytes))
    nocomp_pubkey_txt = encode_b64(nocomp_pubkey_bytes)
    print("no compressed public key = {}".format(nocomp_pubkey_txt))

    address = encode_address(nocomp_pubkey_bytes)
    print("no compressed address = {}".format(address))
    assert address != str(acc.address)

    p2p_pubkey_bytes_head = "\x08\x02\x12".encode("latin-1")
    print("int(p2p public key head bytes) = {}".format(bytes_to_int_str(p2p_pubkey_bytes_head)))

    p2p_pubkey_bytes = p2p_pubkey_bytes_head \
                       + len(pubkey_bytes).to_bytes(length=1, byteorder='big') \
                       + pubkey_bytes
    print("bytes(p2p public key) = {}".format(p2p_pubkey_bytes))
    print("int(p2p public key bytes) = {}".format(bytes_to_int_str(p2p_pubkey_bytes)))
    pubkey_txt = encode_b64(p2p_pubkey_bytes)
    print("p2p public key = {}".format(pubkey_txt))

    p2p_id_bytes = "\x00\x25".encode("latin-1") + p2p_pubkey_bytes
    print("int(p2p id bytes) = {}".format(bytes_to_int_str(p2p_id_bytes)))
    id = encode_b58(p2p_id_bytes)
    print("p2p id = {}".format(id))


def test_private_key():
    acc = Account.decrypt_account(exported_key, '1234')
    assert str(acc.address) == "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"

    acc2 = Account(private_key=bytes(acc.private_key))
    assert bytes(acc.address) == bytes(acc2.address)
    assert str(acc.address) == str(acc2.address)

    acc3 = Account(private_key=str(acc.private_key))
    assert bytes(acc.address) == bytes(acc3.address)
    assert str(acc.address) == str(acc3.address)


def test_json():
    acc = Account.decrypt_account(exported_key, '1234')
    assert str(acc.address) == "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"

    acc_json = acc.json()
    assert acc_json.get('priv_key', None) is None
    assert acc_json.get('enc_key', None) is None
    assert acc_json.get('address', None) == str(acc.address)
    assert acc_json.get('balance', None) == "0 aer"
    assert acc_json.get('nonce', None) == "-1"
    assert acc_json.get('state', None) is None
    assert acc_json.get('is_state_proof', None) is False

    acc2 = Account(private_key=bytes(acc.private_key))
    acc2_json = acc2.json(with_private_key=True)
    assert acc2_json.get('priv_key', None) == str(acc.private_key)
    assert acc2_json.get('enc_key', None) is None
    assert acc2_json.get('address', None) == str(acc.address)

    acc2_json2 = acc2.json(password='1234')
    assert acc2_json2.get('priv_key', None) is None
    assert acc2_json2.get('enc_key', None) == exported_key_str
    assert acc2_json2.get('address', None) == str(acc.address)

    acc3 = Account.from_json(acc_json)
    assert acc3.private_key is None
    assert bytes(acc.address) == bytes(acc3.address)
    assert str(acc.address) == str(acc3.address)

    acc3_json = acc3.json(with_private_key=True)
    assert acc3_json.get('priv_key', None) is None
    assert acc3_json.get('enc_key', None) is None
    assert acc3_json.get('address', None) == str(acc.address)

    acc3_json2 = acc3.json(password='1234')
    assert acc3_json2.get('priv_key', None) is None
    assert acc3_json2.get('enc_key', None) is None
    assert acc3_json2.get('address', None) == str(acc.address)

    acc4 = Account.from_json(acc2_json)
    assert bytes(acc.private_key) == bytes(acc4.private_key)
    assert str(acc.private_key) == str(acc4.private_key)
    assert bytes(acc.address) == bytes(acc4.address)
    assert str(acc.address) == str(acc4.address)
    assert bytes(acc3.address) == bytes(acc4.address)
    assert str(acc3.address) == str(acc4.address)

    acc5 = Account.from_json(acc2_json2, password='1234')
    assert bytes(acc.private_key) == bytes(acc5.private_key)
    assert str(acc.private_key) == str(acc5.private_key)
    assert bytes(acc.address) == bytes(acc5.address)
    assert str(acc.address) == str(acc5.address)
    assert bytes(acc3.address) == bytes(acc5.address)
    assert str(acc3.address) == str(acc5.address)


def test_from_json():
    private_key_str = "47DTHPaRpbJ67KZvBaciz68EJ5k6E2FNBUuknKR6NA4t8oyA3uyvjS2QKxJ7JsgHMunPUitoT"
    private_key = decode_private_key(private_key_str)
    acc = Account.decrypt_account(encrypted_bytes=private_key, password='1234')
    assert str(acc.address) == "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad"

    acc2_json_str = '{"address": "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad", "balance": "99999999999999999999999820 aer", "nonce": "18", "state": {"nonce": "18", "balance": "UrfS3MgM0uP//0w="}, "is_state_proof": false, "enc_key": "47QHSuhBTZ4b7nbw2zJz5EARyQ4XS8gDxhFDeu5mYeKNqfHhwRutUmja3WRxV1suB12eWBeDZ"}'
    acc2 = Account.from_json(data=acc2_json_str, password='5678')
    assert bytes(acc.private_key) == bytes(acc2.private_key)
    assert str(acc.private_key) == str(acc2.private_key)
    assert bytes(acc.address) == bytes(acc2.address)
    assert str(acc.address) == str(acc2.address)
    assert acc2.nonce == 18
    assert str(acc2.balance) == "99999999999999999999999820 aer"
    assert acc2.balance.aergo == "99999999.99999999999999982 aergo"
    assert acc2.balance.gaer == "99999999999999999.99999982 gaer"
    assert acc2.balance.aer == "99999999999999999999999820 aer"

    acc3_json_str = '{"address": "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad", "balance": "100 aergo", "nonce": "7", "state": {"nonce": "20", "balance": "UrfS3MgM0uP//0w=", "unknown_field": "1234"}, "is_state_proof": false, "enc_key": "47QHSuhBTZ4b7nbw2zJz5EARyQ4XS8gDxhFDeu5mYeKNqfHhwRutUmja3WRxV1suB12eWBeDZ"}'
    acc3 = Account.from_json(data=acc3_json_str, password='5678')
    assert bytes(acc.private_key) == bytes(acc3.private_key)
    assert str(acc.private_key) == str(acc3.private_key)
    assert bytes(acc.address) == bytes(acc3.address)
    assert str(acc.address) == str(acc3.address)
    assert acc3.nonce == 20
    assert str(acc3.balance) == "99999999999999999999999820 aer"
    assert acc3.balance.aergo == "99999999.99999999999999982 aergo"
    assert acc3.balance.gaer == "99999999999999999.99999982 gaer"
    assert acc3.balance.aer == "99999999999999999999999820 aer"

    # if is_state_proof == True, "state" will be ignored.
    acc4_json_str = '{"address": "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad", "balance": "100 aergo", "nonce": "7", "state": {"nonce": "20", "balance": "UrfS3MgM0uP//0w=", "unknown_field": "1234"}, "is_state_proof": true, "enc_key": "47QHSuhBTZ4b7nbw2zJz5EARyQ4XS8gDxhFDeu5mYeKNqfHhwRutUmja3WRxV1suB12eWBeDZ"}'
    acc4 = Account.from_json(data=acc4_json_str, password='5678')
    assert bytes(acc.private_key) == bytes(acc4.private_key)
    assert str(acc.private_key) == str(acc4.private_key)
    assert bytes(acc.address) == bytes(acc4.address)
    assert str(acc.address) == str(acc4.address)
    assert acc4.nonce == -1
    assert str(acc4.balance) == "0 aer"
    assert acc4.balance.aergo == "0 aergo"
    assert acc4.balance.gaer == "0 gaer"
    assert acc4.balance.aer == "0 aer"

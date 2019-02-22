import pytest

import ecdsa
import hashlib

from aergo.herapy.obj.address import Address
from aergo.herapy.obj.private_key import PrivateKey
from aergo.herapy.utils.signature import uncompress_key
from aergo.herapy.utils.encoding import encode_address, decode_address


def test_compare_pubkey():
    private_key = "6i2n6TAtsKBaWSujYFzqkBCiP834j1u3nwmffZb8dxCxDcQaXAb"
    address = "AmLnc5nhXjL3a3GUzv1Hb44LnGPvhZufDZ8s8oE9kazgbW6FgnUa"

    pubkey_compressed = decode_address(address).hex()
    pubkey_uncompressed = uncompress_key(pubkey_compressed)
    pubkey_str = bytes.fromhex(pubkey_uncompressed)
    pubkey_bytes = bytes.fromhex(pubkey_uncompressed)[1:]
    pubkey_bytes_x = pubkey_bytes[:ecdsa.SECP256k1.baselen]
    pubkey_bytes_y = pubkey_bytes[ecdsa.SECP256k1.baselen:]
    pubkey_x = ecdsa.util.string_to_number(pubkey_bytes_x)
    pubkey_y = ecdsa.util.string_to_number(pubkey_bytes_y)
    assert ecdsa.ecdsa.point_is_valid(ecdsa.SECP256k1.generator, pubkey_x, pubkey_y)

    pubkey_point = ecdsa.ellipticcurve.Point(ecdsa.SECP256k1.curve, pubkey_x, pubkey_y, ecdsa.SECP256k1.order)
    pubkey = ecdsa.ecdsa.Public_key(ecdsa.SECP256k1.generator, pubkey_point)

    pk = PrivateKey(pk=private_key)
    pk_pubkey = pk.public_key
    pk_pubkey_str = pk.get_public_key(compressed=False)

    assert address == str(pk.address)
    assert pubkey.point == pk_pubkey.point
    assert pubkey_str == pk_pubkey_str

    pk_pubkey_str = pk.get_public_key()
    assert address == encode_address(pk_pubkey_str)

    addr = Address(pubkey=None, address=address)
    addr_pubkey = addr.public_key
    addr_pubkey_str = addr.get_public_key(compressed=False)

    assert pubkey.point == addr_pubkey.point
    assert pubkey_str == addr_pubkey_str

    addr_pubkey_str = addr.get_public_key()
    assert address == encode_address(addr_pubkey_str)

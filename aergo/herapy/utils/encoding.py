import base58
import base64

from ..constants import *


def encode_address(address):
    v = ADDRESS_VERSION + address
    return base58.b58encode_check(v).decode('utf-8')


def decode_address(address):
    v = base58.b58decode_check(address)
    return v[len(ADDRESS_VERSION):]


def encode_private_key(private_key):
    v = PRIVATE_KEY_VERSION + private_key
    return base58.b58encode_check(v).decode('utf-8')


def decode_private_key(private_key):
    v = base58.b58decode_check(private_key)
    return v[len(PRIVATE_KEY_VERSION):]


def encode_signature(sign):
    return base64.b64encode(sign)


def encode_hash(v):
    return base64.b64encode(v)


def decode_hash(v):
    return base64.b64decode(v, validate=True)

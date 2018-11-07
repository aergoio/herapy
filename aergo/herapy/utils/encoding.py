import base58
import base64

from herapy.constants import ACCOUNT_PREFIX


def encode_address(address):
    return base58.b58encode_check(bytes([ACCOUNT_PREFIX]) + address)


def decode_address(base58_address):
    decoded = base58.b58decode_check(base58_address)
    return decoded[1:]


def encode_hash(hash):
    return base64.b64encode(hash)


def encode_signature(sig):
    return base64.b64encode(sig)


def decode_hash(hash):
    return base64.b64decode(hash, validate=True)

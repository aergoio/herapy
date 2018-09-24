import base58

from herapy.constants import ACCOUNT_PREFIX


def encode_address(address):
    return base58.b58encode_check(bytes([ACCOUNT_PREFIX]) + address)


def decode_address(base58_address):
    decoded = base58.b58decode_check(base58_address)
    return decoded[1:]

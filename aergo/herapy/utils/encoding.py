# -*- coding: utf-8 -*-

import base58
import base64

from ..constants import *


def encode_address(address):
    v = ADDRESS_VERSION + address
    return base58.b58encode_check(v).decode('utf-8')


def decode_address(address):
    v = base58.b58decode_check(address)
    return v[len(ADDRESS_VERSION):]

def decode_root(root):
    return base58.b58decode(root)


def encode_payload(payload):
    return encode_address(payload)


def decode_payload(payload_str):
    return decode_address(payload_str)


def encode_private_key(private_key):
    v = PRIVATE_KEY_VERSION + private_key
    return base58.b58encode_check(v).decode('utf-8')


def decode_private_key(private_key):
    v = base58.b58decode_check(private_key)
    return v[len(PRIVATE_KEY_VERSION):]


def encode_signature(sign):
    return base64.b64encode(sign)


def encode_tx_hash(tx_hash):
    return base58.b58encode(tx_hash).decode('utf-8')


def decode_tx_hash(tx_hash):
    return base58.b58decode(tx_hash)


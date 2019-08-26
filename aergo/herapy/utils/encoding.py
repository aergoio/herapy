# -*- coding: utf-8 -*-

import base58
import base64
import ecdsa

from ..constants import *


def is_empty(v):
    if v is None or 0 == len(v):
        return True
    return False


def encode_b64(v):
    if is_empty(v):
        return None
    return base64.b64encode(v).decode('utf-8')


def decode_b64(v):
    if is_empty(v):
        return None
    return base64.b64decode(v)


def encode_b58_check(v):
    if is_empty(v):
        return None
    return base58.b58encode_check(v).decode('utf-8')


def decode_b58_check(v):
    if is_empty(v):
        return None
    return base58.b58decode_check(v)


def encode_b58(v):
    if is_empty(v):
        return None
    return base58.b58encode(v).decode('utf-8')


def decode_b58(v):
    if is_empty(v):
        return None
    return base58.b58decode(v)


def encode_address(address):
    v = ADDRESS_VERSION + address
    return encode_b58_check(v)


def decode_address(address):
    if is_empty(address):
        return None
    v = decode_b58_check(address)
    return v[len(ADDRESS_VERSION):]

def decode_root(root):
    if is_empty(root):
        return None
    return base58.b58decode(root)


def encode_payload(payload):
    if is_empty(payload):
        return None
    return encode_b58_check(payload)


def decode_payload(payload_str):
    if is_empty(payload_str):
        return None
    return decode_b58_check(payload_str)


def encode_private_key(private_key):
    v = PRIVATE_KEY_VERSION + private_key
    return encode_b58_check(v)


def decode_private_key(private_key):
    if is_empty(private_key):
        return None
    v = decode_b58_check(private_key)
    return v[len(PRIVATE_KEY_VERSION):]


def encode_tx_hash(tx_hash):
    if is_empty(tx_hash):
        return None
    return encode_b58(tx_hash)


def decode_tx_hash(tx_hash):
    if is_empty(tx_hash):
        return None
    return decode_b58(tx_hash)


def encode_signature(sign):
    if is_empty(sign):
        return None
    return encode_b58(sign)


def decode_signature(sign):
    if is_empty(sign):
        return None
    return decode_b58(sign)


def decode_public_key(public_key, curve=ecdsa.SECP256k1):
    v = decode_address(public_key)
    head = v[:1]
    x_bytes = v[1:curve.baselen]

    if PUBLIC_KEY_UNCOMPRESSED == head:
        y_bytes = v[curve.baselen+1:]
    else:
        y_bytes = None
    return head, x_bytes, y_bytes


def encode_block_hash(block_hash):
    if is_empty(block_hash):
        return None
    return encode_b58(block_hash)


def decode_block_hash(block_hash):
    if is_empty(block_hash):
        return None
    return decode_b58(block_hash)

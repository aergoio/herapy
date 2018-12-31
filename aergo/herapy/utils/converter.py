# -*- coding: utf-8 -*-

"""Common utility module for converting types."""

import json
import base58
import toml
import socket

from ..obj.aergo_conf import AergoConfig
from ..grpc import blockchain_pb2
from .encoding import encode_address, encode_tx_hash


def convert_toml_to_aergo_conf(v):
    aergo_conf = AergoConfig()

    conf = toml.loads(v)
    for k, v in conf.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                aergo_conf.add_conf(k2, v2, k)
        else:
            aergo_conf.add_conf(k, v)

    return aergo_conf


def convert_aergo_conf_to_toml(aergo_conf):
    return toml.dumps(aergo_conf.conf)


def convert_tx_to_grpc_tx(tx):
    grpc_tx = blockchain_pb2.Tx()
    grpc_tx.hash = bytes(tx.tx_hash)
    if tx.nonce is not None:
        grpc_tx.body.nonce = tx.nonce
    if tx.from_address is not None:
        grpc_tx.body.account = bytes(tx.from_address)
    if tx.to_address is not None:
        grpc_tx.body.recipient = bytes(tx.to_address)
    if tx.amount is not None:
        grpc_tx.body.amount = bytes(tx.amount)
    if tx.payload is not None:
        grpc_tx.body.payload = tx.payload
    grpc_tx.body.limit = tx.fee_limit
    grpc_tx.body.price = bytes(tx.fee_price)
    grpc_tx.body.type = tx.tx_type.value
    if tx.sign is not None:
        grpc_tx.body.sign = tx.sign
    return grpc_tx


def convert_tx_to_json(tx):
    if tx is None:
        return None

    return tx.json()


def convert_tx_to_formatted_json(tx):
    if tx is None:
        return None

    return json.dumps(convert_tx_to_json(tx), indent=2)


def convert_bytes_to_int_str(v):
    return ''.join('{:d} '.format(x) for x in v)


def convert_bytes_to_hex_str(v):
    return ''.join('0x{:02x} '.format(x) for x in v)


def convert_ip_bytes_to_str(v):
    l = len(v)

    # IPv4
    if 4 == l:
        return socket.inet_ntoa(v)
    elif 16 == l and all(v2 == 0 for v2 in list(v[:10])) and 255 == v[10] and 255 == v[11]:
        return socket.inet_ntoa(v[12:16])

    # IPv6
    return socket.inet_ntop(socket.AF_INET6, v)


""" Deprecated
def convert_luajson_to_json(v):
    v = v.decode('utf-8').replace('\\', '')
    v = v[1:len(v)-1]
    return json.loads(v)
"""

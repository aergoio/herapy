# -*- coding: utf-8 -*-

"""Common utility module for converting types."""

import json
import base58

from ..grpc import blockchain_pb2
from .encoding import encode_address, encode_tx_hash


def convert_tx_to_grpc_tx(tx):
    grpc_tx = blockchain_pb2.Tx()
    grpc_tx.hash = bytes(tx.tx_hash)
    if tx.nonce is not None:
        grpc_tx.body.nonce = tx.nonce
    if tx.from_address is not None:
        grpc_tx.body.account = tx.from_address
    if tx.to_address is not None:
        grpc_tx.body.recipient = tx.to_address
    if tx.amount is not None:
        grpc_tx.body.amount = tx.amount
    if tx.payload is not None:
        grpc_tx.body.payload = tx.payload
    grpc_tx.body.limit = tx.fee_limit
    grpc_tx.body.price = tx.fee_price
    grpc_tx.body.type = tx.tx_type
    if tx.sign is not None:
        grpc_tx.body.sign = tx.sign
    return grpc_tx


def convert_tx_to_json(tx):
    if tx is None:
        return None

    json_tx = {
        'hash': str(tx.tx_hash)
    }

    body = {
        'nonce': tx.nonce,
        'from': encode_address(tx.from_address),
        'amount': tx.amount,
        'fee_limit': tx.fee_limit,
        'fee_price': tx.fee_price,
        'tx_type': tx.tx_type,
        'tx_sign': tx.sign_str
    }

    if tx.payload is not None:
        body['payload'] = str(base58.b58encode_check(tx.payload))

    if tx.to_address is not None:
        body['to'] = encode_address(tx.to_address)

    json_tx['body'] = body

    return json_tx


def convert_tx_to_formatted_json(tx):
    if tx is None:
        return None

    return json.dumps(convert_tx_to_json(tx), indent=2)


def convert_bytes_to_int_str(v):
    return ''.join('{:d} '.format(x) for x in v)


def convert_bytes_to_hex_str(v):
    return ''.join('0x{:02x} '.format(x) for x in v)


def convert_luajson_to_json(v):
    v = v.decode('utf-8').replace('\\', '')
    v = v[1:len(v)-1]
    return json.loads(v)

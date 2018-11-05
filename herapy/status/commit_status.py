# -*- coding: utf-8 -*-

"""Enumeration of Commit Status."""

import enum

from ..grpc import rpc_pb2


@enum.unique
class CommitStatus(enum.IntEnum):
    """
    TX_OK = 0
    TX_NONCE_TOO_LOW = 1
    TX_ALREADY_EXISTS = 2
    TX_INVALID_HASH = 3
    TX_INVALID_SIGN = 4
    TX_INVALID_FORMAT = 5
    TX_INSUFFICIENT_BALANCE = 6
    TX_HAS_SAME_NONCE = 7
    TX_INTERNAL_ERROR = 9
    """
    TX_OK = rpc_pb2.TX_OK
    TX_NONCE_TOO_LOW = rpc_pb2.TX_NONCE_TOO_LOW
    TX_ALREADY_EXISTS = rpc_pb2.TX_ALREADY_EXISTS
    TX_INVALID_HASH = rpc_pb2.TX_INVALID_HASH
    TX_INVALID_SIGN = rpc_pb2.TX_INVALID_SIGN
    TX_INVALID_FORMAT = rpc_pb2.TX_INVALID_FORMAT
    TX_INSUFFICIENT_BALANCE = rpc_pb2.TX_INSUFFICIENT_BALANCE
    TX_HAS_SAME_NONCE = rpc_pb2.TX_HAS_SAME_NONCE
    TX_INTERNAL_ERROR = rpc_pb2.TX_INTERNAL_ERROR


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
import base58
import grpc
import rpc

from herapy.utils.encoding import encode_address, decode_address


@pytest.fixture()
def setup():
    pytest.rpc = rpc.Rpc('localhost:7845') # server must be running!
    pytest.passphrase = 'passphrase'
    pytest.address = pytest.rpc.create_account(pytest.passphrase)


# TODO: better way to validate addresses?
def validate_address(address):
    assert pytest.address == encode_address(decode_address(pytest.address)) # did we get a proper b58-encoded address?


def test_create_account(setup):
    validate_address(pytest.address)


def test_get_accounts(setup):
    [validate_address(a) for a in pytest.rpc.get_accounts()]

# TODO: what does 'locking' do to the account? Which operations are disallowed when in locked state?
# TODO: Would be good to test for these.

# We know that we cannot send transactions from a locked account.
def test_lock(setup):
    address = pytest.rpc.lock(pytest.address, pytest.passphrase)
    validate_address(address)
    try:
        pytest.rpc.lock(pytest.address, 'wrongpassphrase')
    except grpc.RpcError as e:
        assert e.details() == 'address or password is incorrect'


def test_unlock(setup):
    address = pytest.rpc.unlock(pytest.address, pytest.passphrase)
    validate_address(address)
    try:
        pytest.rpc.unlock(pytest.address, 'wrongpassphrase')
    except grpc.RpcError as e:
        assert e.details() == 'address or password is incorrect'

# TODO test cases:
# Can we send a transaction with value of zero? Less than zero? to and from the same account? To and from nonexistent or
# improperly formatted accounts? Check Transaction for type errors.


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
import base58

import rpc

@pytest.fixture()
def setup():
    pytest.rpc = rpc.Rpc('localhost:7845') # server must be running!

def test_create_account(setup):
    address = pytest.rpc.create_account('passphrase')
    assert address == base58.b58encode_check(base58.b58decode_check(address)) # test that we got a valid b58 address
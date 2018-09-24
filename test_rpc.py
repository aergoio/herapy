#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
import base58
import rpc

from herapy.utils.encoding import encode_address, decode_address

@pytest.fixture()
def setup():
    pytest.rpc = rpc.Rpc('localhost:7845') # server must be running!

def test_create_account(setup):
    address = pytest.rpc.create_account('passphrase')
    assert address == encode_address(decode_address(address)) # test that we got a properly encoded address
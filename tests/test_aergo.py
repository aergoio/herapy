# -*- coding: utf-8 -*-

"""Tests for `aergo` package."""

import pytest
import base58

from herapy.aergo import Aergo


@pytest.fixture
def setup():
    pass


def test_create_new_account(setup):
    # check a result with 'aergocli'
    # 1. get password
    password = "test_password"
    # 2. make a private key
    aergo = Aergo()
    account = aergo.create_account(password)
    private_key = account.private_key
    print("Private Key = {}".format(private_key))
    print("base58(Private Key) = {}".format(base58.b58encode_check(private_key)))
    # 3. get a public key
    # 4. get an address

def test_account_state():
    aergo = Aergo()
    aergo.connect('localhost:7845')
    password = "test_password"
    account = aergo.create_account(password)
    state = aergo.get_account_state(account)
    print(f"Account state = {state}")
    aergo.disconnect()
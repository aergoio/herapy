# -*- coding: utf-8 -*-

"""Tests for `aergo` package."""

import pytest
import base58

from herapy.aergo import Aergo


@pytest.fixture
def setup():
    pass


def test_create_new_account(setup):
    # TODO fill this function
    # check a result with 'aergocli'
    # 1. get password
    password = "test_password"
    # 2. make a private key
    aergo = Aergo()
    account = aergo.create_account(password)
    private_key = account.secret_key
    print("Private Key = {}".format(private_key))
    print("base58(Private Key) = {}".format(base58.b58encode_check(private_key)))
    # 3. get a public key
    # 4. get an address


@pytest.mark.skip(reason="import accounts not supported")
def test_import_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. extract a private key
    # 5. generate a public key and address
    # 6. compare the public key and address from 'aergocli'
    pass


@pytest.mark.skip(reason="Lock and unlock account not supported")
def test_lock_and_unlock_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. lock an account_old and check status
    # 5. unlock the account_old and check status
    pass

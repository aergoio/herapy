#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

from pathlib import Path
from subprocess import run
import os
import pprint

import pytest

from herapy import herapy
from herapy.account.account import Account
from herapy.transaction import transaction

@pytest.fixture
def setup():
    pytest.aergo = herapy.Herapy('localhost:7845')

def test_create_new_account(setup):
    pytest.aergo.save_keys('ecdsa') # generates ecdsa.public.pem and ecdsa.private.pem
    assert Path("ecdsa.public.pem").is_file() and Path("ecdsa.private.pem").is_file()
    address = pytest.aergo.create_account('passphrase')
    assert isinstance(address, bytes)
    os.remove("ecdsa.public.pem")
    os.remove("ecdsa.private.pem")

def get_accounts_from_aergocli(username="[YOUR_USERNAME_HERE]"):
    aergocli_path = f"/Users/{username}/go/src/github.com/aergoio/aergo/bin/aergocli"
    assert Path(aergocli_path).is_file()

    cmd = run([aergocli_path, "account", "list"], capture_output=True)
    accounts = cmd.stdout.decode("utf-8").split(", ")
    accounts[0] = accounts[0][1:]
    accounts[-1] = accounts[-1][:-2]
    return accounts


def test_import_accounts():
    print(get_accounts_from_aergocli("harlan"))
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. extract a private key
    # 5. generate a public key and address
    # 6. compare the public key and address from 'aergocli'
    pass

@pytest.mark.skip(reason="Lock and unlock not supported")
def test_lock_and_unlock_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. lock an account and check status
    # 5. unlock the account and check status
    pass

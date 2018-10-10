#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest

from herapy import herapy
from herapy.account import account
from herapy.transaction import transaction

#def test_sign_transaction():
#    account = herapy.account.Account()
#    account.sign_transaction( transaction.Transaction("") )

def test_create_new_account():
    # TODO fill this function
    # check a result with 'aergocli'
    # 1. get password
    # 2. make a private key
    # 3. get a public key
    # 4. get an address
    pass

def test_import_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. extract a private key
    # 5. generate a public key and address
    # 6. compare the public key and address from 'aergocli'
    pass

def test_lock_n_unlock_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. lock an account and check status
    # 5. unlock the account and check status
    pass


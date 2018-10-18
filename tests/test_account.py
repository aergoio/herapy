# -*- coding: utf-8 -*-

"""Tests for `aergo.account` package."""

import pytest
import base58

from herapy.account import Account


def test_create_new_account():
    # TODO fill this function
    # check a result with 'aergocli'
    # 1. get password
    password = "test_password"
    # 2. make a new private key
    account = Account(password)
    private_key = account.private_key
    print("Private Key = {}".format(private_key))
    print("Private Key string = {}".format(account.private_key_str))
    # 3. get a public key
    public_key = account.public_key
    print("public key = {}".format(public_key))
    # 4. get an address
    address = account.address
    print("address = {}".format(address))
    print("address string = {}".format(account.address_str))


def test_get_account_from_privkey():
    # 1. get password
    password = "test_password"
    # 2. get private key
    private_key_str = "26ccNqpXhox8kYo6YfssiKSxaXFWXgieSbyhrCKfLUJH8bas7A7"
    # 3. import the private key
    account = Account(password, private_key_str)
    # 4. check the public key
    public_key = account.public_key
    print("public key = {}".format(public_key))
    point = public_key.point
    print("    x = {}".format(point.x()))
    print("    y = {}".format(point.y()))
    assert point.x() == 85322853754860988965170721342962646872483704484369335458444547479171026481193
    assert point.y() == 37956043211170965023446802410195120686094681654219278351383101739484381476284
    # 5. check the address
    print("address = {}".format(account.address))
    print("str(address) = {}".format(account.address_str))
    assert account.address_str == "AmMwJUkRX6pcR7MA9iMMrvCT4DLLwi11HnQAZMWujr8imXs8YbSm"


def test_get_account_from_address():
    # 1. get password
    password = "password is nothing"
    # 2. get address
    address = "AmP9NdFPwGhKiedBq5qZH1yyxr1WCtY8pn6CRurRsaQiCA6KwANf"
    # 3. import the address
    account = Account(password, empty=True)
    account.address = address
    # 4. check the address
    print("address = {}".format(account.address))
    print("str(address) = {}".format(account.address_str))
    assert account.address_str == address


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


@pytest.mark.skip(reason="export accounts not supported")
def test_export_accounts():
    # TODO fill this function
    # 1. export accounts
    # 2. import exported file using 'aergocli'
    pass



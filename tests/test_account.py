# -*- coding: utf-8 -*-

"""Tests for `aergo.account` package."""

import pytest
import base58

from herapy.account import Account


@pytest.fixture
def setup():
    pass


def test_create_new_account(setup):
    # TODO fill this function
    # check a result with 'aergocli'
    # 1. get password
    password = "test_password"
    # 2. make a private key
    account = Account(password)
    account.generate_new_key()
    private_key = account.private_key
    print("Private Key = {}".format(private_key))
    print("base58(Private Key) = {}".format(base58.b58encode_check(private_key)))
    # 3. get a public key
    public_key = account.public_key
    print("public key = {}".format(public_key))
    # 4. get an address
    address = account.address
    print("address = {}".format(address))
    print("hex(address) = {}".format(address.hex()))


def test_import_privkey():
    # 1. get password
    password = "test_password"

    # 2. get private key
    private_key_str = "28wuAWLrQCZ9dfpM2sQQQkMEqmUFafLWZ8V7DbJCxgFaAtiwVF"
    private_key_bytes = base58.b58decode_check(private_key_str)

    # 3. create Account
    account = Account(password)

    # 4. import the private key
    account.private_key = private_key_bytes

    # 5. check the public key
    public_key = account.public_key
    print("public key = {}".format(public_key))
    point = public_key.point
    print("    x = {}".format(point.x()))
    print("    y = {}".format(point.y()))
    assert point.x() == 54931674066989017913690710436868039247394534957568781144902447317688277357288
    assert point.y() == 107308612991485468160937992965052330228024358581729857325878253018954673441678

    # 6. check the address
    address = account.address
    print("address = {}".format(address))
    print("hex(address) = {}".format(address.hex()))
    assert address.hex() == "02797239c92b17458b88155fe668f7acb3621febefefc930de3bc5312278dd52e8"
    address_str = account.address_str
    print("address str = {}".format(address_str))
    assert address_str == "AmMRiBguPQB2eZQxE7XnT77hu757QFRv6ReC3VHDi96Dh3S4mYDz"


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


@pytest.mark.skip(reason="Lock and unlock account not supported")
def test_lock_and_unlock_accounts():
    # TODO fill this function
    # 1. export accounts using 'aergocli'
    # 2. import exported file
    # 3. get accounts
    # 4. lock an account_old and check status
    # 5. unlock the account_old and check status
    pass

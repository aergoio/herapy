#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for grpc package."""

import pytest


# from herapy.grpc import account_pb2
# from herapy.grpc import blockchain_pb2
# from herapy.grpc import rpc_pb2


@pytest.mark.skip(reason='grpc imports')
def test_grpc_rpc(response):
    person = rpc_pb2.Personal()
    person.passphrase = 'test'

    person.account.address = "PERSONAL ACCOUNT #1".encode()

    assert person.account.address.decode() == "PERSONAL ACCOUNT #1"


@pytest.mark.skip(reason='grpc imports')
def test_grpc_account(response):
    account_list = account_pb2.AccountList()

    # add an account_old
    acc1 = account_list.accounts.add()
    acc1.address = "ACCOUNT #1".encode()

    # add an account_old
    acc2 = account_list.accounts.add()
    acc2.address = "ACCOUNT #2".encode()

    # print account_old list
    print("All addresses are %s" % account_list.SerializeToString())
    """
    idx = 0
    for acc in account_list.accounts:
        print("#%d addresses is '%s'" % (idx, acc.address.decode()))
        idx += 1
    """

    # check account_old list
    assert acc1.address == account_list.accounts[0].address
    assert acc1.address.decode() == "ACCOUNT #1"
    assert account_list.accounts[0].address.decode() == "ACCOUNT #1"

    assert acc2.address == account_list.accounts[1].address
    assert acc2.address.decode() == "ACCOUNT #2"
    assert account_list.accounts[1].address.decode() == "ACCOUNT #2"


@pytest.mark.skip(reason='grpc imports')
def test_grpc_blockchain(response):
    # block
    block1 = blockchain_pb2.Block()

    # block header
    block1_header = block1.header
    block1_header.blockNo = 1

    # block body
    block1_body = block1.body

    # add tx
    tx1 = block1_body.txs.add()
    tx1.body.type = blockchain_pb2.NORMAL

    # add tx
    tx2 = block1_body.txs.add()
    tx2.body.type = blockchain_pb2.GOVERNANCE

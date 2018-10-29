# -*- coding: utf-8 -*-

"""Tests for `aergo` package."""

import pytest
from pytest_mock import mocker

from herapy.aergo import Aergo
from herapy.transaction import Transaction


@pytest.fixture
def setup():
    pytest.aergo = Aergo()
    pytest.aergo.connect('localhost:7845')

    pytest.sender = pytest.aergo.create_account("passphrase")
    pytest.receiver = pytest.aergo.create_account("passphrase")

    pytest.transaction = Transaction(hash=b"",
                     nonce=1,
                     from_address=pytest.sender.address,
                     to_address=pytest.receiver.address,
                     amount=1,
                     payload=b"",
                     signature=b"",
                     type=0,
                     limit=0,
                     price=0)

    pytest.aergo.unlock_account(address=pytest.sender.address, passphrase="passphrase")

def test_create_account(setup):
    account = pytest.aergo.create_account("passphrase")
    print(f"Created Account {account}")

def test_sign_tx(setup):
    transaction = pytest.transaction
    tx = transaction.to_tx()
    signed_tx = pytest.aergo.sign_tx(tx)
    assert tx.body.sign is not None
    print(f"Tx {tx.hash} has signature {tx.body.sign}")


def test_send(setup):
    result = pytest.aergo.send(from_address=pytest.sender.address,
                               to_address=pytest.receiver.address,
                               amount=1,
                               payload=b"",
                               limit=0,
                               price=0)
    print(f"Tx hash: {result.hash}")

def test_send_tx(setup):
    pytest.aergo.unlock_account(address=pytest.sender.address, passphrase="passphrase")
    transaction = pytest.transaction

    tx = transaction.to_tx()

    signed_tx = pytest.aergo.sign_tx(tx)
    result = pytest.aergo.send_tx(signed_tx)
    tx_hash = result.hash

    print(f"Sent transaction: {pytest.aergo.get_tx(tx_hash)}")

def test_commit_tx(setup):
    sender = pytest.aergo.create_account("passphrase")
    receiver = pytest.aergo.create_account("passphrase")
    pytest.aergo.unlock_account(address=sender.address, passphrase="passphrase")
    transaction = pytest.transaction

    tx = transaction.to_tx()

    signed_tx = pytest.aergo.sign_tx(tx)

    txs = [signed_tx, signed_tx, signed_tx]
    result = pytest.aergo.commit_tx(txs=txs)
    print(result) # TODO investigate these "invalid hash" results


def test_get_account_info(setup):
    account = pytest.aergo.create_account("passphrase")
    print(f"Account: {account.address}")

    accounts = pytest.aergo.get_node_accounts()
    print(f"There are {len(accounts)} accounts")
    for account in accounts:
        print(f"Account {account.address_str} has state {pytest.aergo.get_account_state(account)}")

    peers = pytest.aergo.get_peers().peers
    print(f"There are {len(peers)} peers")
    for peer in peers:
        print(f"Peer: {peer}")
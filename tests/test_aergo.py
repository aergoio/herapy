# -*- coding: utf-8 -*-

"""Tests for `aergo` package."""

import pytest
from pytest_mock import mocker

from herapy.aergo import Aergo
from herapy.transaction import Transaction


@pytest.fixture
def setup():
    pass

def test_all():
    aergo = Aergo()
    aergo.connect('localhost:7845')
    account = aergo.create_account('passphrase')

    print()
    print(f"Account: {account.address}")

    accounts = aergo.get_node_accounts()
    print(f"There are {len(accounts)} accounts")
    for account in accounts:
        print(f"Account state: {aergo.get_account_state(account)}")

    peers = aergo.get_peers().peers
    print(f"There are {len(peers)} peers")
    for peer in peers:
        print(f"Peer: {peer}")

    tx = Transaction(hash="",
                     nonce=0,
                     from_address="",
                     to_address="",
                     amount=0,
                     payload="",
                     signature="",
                     type="")
    signed_tx = aergo.sign_tx(tx.concatenate_fields())
    print(f"Signed tx: {signed_tx}")

    print(aergo.send_tx(tx))
    print(aergo.commit_tx(tx))

    tx_0 = aergo.get_tx(b'0')
    print(f"{tx_0}")

    aergo.disconnect()


def test_create_new_account(setup):
    # 1. make aergo instance
    aergo = Aergo()
    assert aergo.account is None
    # 2. connect
    aergo.connect("mocking_target")
    # 3. get blockchain status
    best_block_hash, best_height = aergo.get_blockchain_status()
    print(best_block_hash)
    print(best_height)

    account = aergo.create_account(password)
    private_key = account.private_key
    print("Private Key = {}".format(private_key))
    print("str(Private Key) = {}".format(account.private_key_str))
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

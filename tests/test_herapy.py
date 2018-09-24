#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy import herapy
from herapy.transaction import transaction
from herapy.blockchain import blockchain

@pytest.fixture
def setup():
    pytest.aergo = herapy.Herapy()

# Accounts
def test_create_address(setup):
    pytest.aergo.create_address('FAIL')

@pytest.mark.skip(reason="WIP")
def test_get_addresses(setup):
    assert pytest.aergo.get_addresses() == []

@pytest.mark.skip(reason="WIP")
def test_sign_transaction(setup):
    pytest.aergo.sign_transaction(transaction.Transaction(payload=""))

def test_send_unsigned_transaction(setup):
    pytest.aergo.send_unsigned_transaction(None)

@pytest.mark.skip(reason="WIP")
def test_send_signed_transaction(setup):
    pytest.aergo.send_signed_transaction(herapy.transaction.Transaction(payload=""))

# Blockchain
def test_get_transaction(setup):
    pytest.aergo.get_transaction('0x0')

def test_get_block_info_by_hash(setup):
    pytest.aergo.get_block_info_by_hash('0x0')
    
def test_get_block_info_by_number(setup):
    pytest.aergo.get_block_info_by_hash('0')
    
def test_best_block_hash_and_number(setup):
    pytest.aergo.best_block_hash('0x0')
    pytest.aergo.best_block_number(0)
    
def test_get_account_nonce(setup):
    pytest.aergo.get_account_nonce('0')

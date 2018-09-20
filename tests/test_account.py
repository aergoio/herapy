#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy import herapy
from herapy.account import account

@pytest.fixture
def setup():
    pytest.account = account.Account(0x0, 0x0)

def test_new_account_has_public_and_private_keys():
    pass

def test_sign_message():
    pass

def test_verify_valid_key():
    pass

def test_verify_invalid_key():
    pass
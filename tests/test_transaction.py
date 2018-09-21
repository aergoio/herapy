#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy.transaction import transaction
from herapy.utils.key_manager import KeyManager

def test_signed():
    tx = transaction.Transaction("")
    assert not tx.is_signed()
    tx.sign_with_key_manager(KeyManager())
    assert tx.is_signed()


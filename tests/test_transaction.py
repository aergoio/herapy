#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy.transaction import transaction
from herapy.utils.key_manager import KeyManager

@pytest.mark.skip(reason='Now supplying signature in Transaction constructor')
def test_signed():
    tx = transaction.Transaction("", "", b"", b"", 0, b"", b"", 0)
    assert not tx.is_signed()
    tx.sign_with_key_manager(KeyManager())
    print(tx.signature)
    assert tx.is_signed()
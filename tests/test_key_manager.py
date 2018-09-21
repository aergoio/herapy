#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
import os

from herapy.utils.key_manager import KeyManager


@pytest.fixture
def setup():
    pytest.km = KeyManager()


def test_keys_created(setup):
    pytest.km.save_keys('ecdsa')
    assert os.path.exists('ecdsa.public.pem')
    assert os.path.exists('ecdsa.private.pem')


def test_valid_signature_succeeds(setup):
    message = "hello"
    sig = pytest.km.sign_message(message)
    assert pytest.km.verify_message("hello", sig)


def test_invalid_signature_fails(setup):
    message = "hello"
    with pytest.raises(AssertionError):
        assert pytest.km.verify_message(message, "FAIL")


def test_keys_deleted(setup):
    pytest.km.save_keys('ecdsa')
    pytest.km.delete_keys('ecdsa')
    assert not os.path.exists('ecdsa.public.pem')
    assert not os.path.exists('ecdsa.private.pem')
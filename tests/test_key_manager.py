#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
import os

from herapy import herapy
from herapy.utils.key_manager import KeyManager

@pytest.fixture
def setup():
    pytest.km = KeyManager()
    pytest.km.generate_and_save_keys("ecdsa")
    pytest.sk = pytest.km.load_signing_key_from_file("ecdsa")
    pytest.vk = pytest.km.load_verifying_key_from_file("ecdsa")

def test_keys_created(setup):
    assert os.path.exists('ecdsa.public.pem')
    assert os.path.exists('ecdsa.private.pem')

def test_valid_signature_succeeds(setup):
    message = "hello"
    sig = pytest.km.sign_message(pytest.sk, message)
    assert pytest.km.verify_message(pytest.vk, "hello", sig)

def test_invalid_signature_fails(setup):
    message = "hello"
    with pytest.raises(AssertionError):
        pytest.km.verify_message(pytest.vk, "hello", "FAIL")

def test_keys_deleted(setup):
    pytest.km.delete_keys("ecdsa")
    assert not os.path.exists('ecdsa.public.pem')
    assert not os.path.exists('ecdsa.private.pem')
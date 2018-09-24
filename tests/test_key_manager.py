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
    correct_sig = b'\x02\x17\x8c\xb9-S\xfd\xf7- g\x9e\xd6\x84_a?\x13O3\x0e\xa3\xfb\xcf\xb8|JS=\xfe\xce\x8f\xaa\xdb\x82\xe1\x86\xed]\x99C\xc6\x9b\xfb\xd3\x0bk\xce\xd2wW/\xbe\xdf\xb2h\xe0\x0b\x93\xe9\x89n&\xc7'
    assert str(sig).__eq__(correct_sig)
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
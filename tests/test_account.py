#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy import herapy
from herapy.account import account

@pytest.fixture
def setup():
    pytest.account = account.Account(0x0, 0x0)


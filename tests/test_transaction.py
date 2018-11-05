#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `herapy` package."""

import pytest
from herapy import transaction

@pytest.mark.skip(reason='Now supplying signature in Transaction constructor')
def test_signed():
    private_key_str = "28wuAWLrQCZ9dfpM2sQQQkMEqmUFafLWZ8V7DbJCxgFaAtiwVF"

    # 1. fix payload
    # 2. make transaction
    # 3. sign transaction
    # 4. verify transaction using 'aergocli'
    pass

def test_verify():
    # 1. fix payload using 'aergocli'
    # 2. make transaction using 'aergocli'
    # 3. sign transaction using 'aergocli'
    # 4. verify transaction
    pass

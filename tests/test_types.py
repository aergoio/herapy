#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for grpc package."""

import pytest


from herapy.types import account_pb2, blockchain_pb2, node_pb2, p2p_pb2, rpc_pb2


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

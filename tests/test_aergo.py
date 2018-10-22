# -*- coding: utf-8 -*-

"""Tests for `aergo` package."""

import pytest
from pytest_mock import mocker

from herapy.aergo import Aergo
from herapy import comm
from herapy.grpc import rpc_pb2


def test_create_new_aergo():
    # check a result with 'aergocli'
    # 1. make aergo instance
    aergo = Aergo()
    assert aergo.account is None
    # 2. connect
    try:
        aergo.connect(None)
    except ValueError as e:
        print(type(e))
        print(str(e))
        assert str(e) == "need target value"


'''
@pytest.mark.parametrize('best_block_hash, best_height', [
    (b'VaMdjKC9eCXcHTSzJLu8B8jD7jNicody88RRYikqnKQwcSCk6', 22512)
])
def test_get_blockchain_status(mocker, best_block_hash, best_height):
    mock_blockchain_status = rpc_pb2.BlockchainStatus()
    print('best_block_hash = %s' % best_block_hash)
    mock_blockchain_status.best_block_hash = best_block_hash
    print('best_height = %d' % best_height)
    mock_blockchain_status.best_height = best_height

    mocker.patch.object(comm, "Comm")
    comm.Comm.connect().return_value = None
    comm.Comm.get_blockchain_status().return_value = mock_blockchain_status

    # check a result with 'aergocli'
    # 1. make aergo instance
    aergo = Aergo()
    assert aergo.account is None
    # 2. connect
    aergo.connect("mocking_target")
    # 3. get blockchain status
    best_block_hash, best_height = aergo.get_blockchain_status()
    print(best_block_hash)
    print(best_height)
'''

import pytest

from aergo.herapy.obj.tx_result import TxResult, TxResultType,\
    TxResultStatus, CommitStatus
from aergo.herapy.grpc import rpc_pb2, blockchain_pb2
from aergo.herapy.utils.encoding import encode_tx_hash, encode_address


def test_grpc_receipt():
    grpc_result1 = blockchain_pb2.Receipt()
    all_fields = grpc_result1.DESCRIPTOR.fields_by_name
    '''
    for key in all_fields.keys():
        one_field = all_fields[key]
        print('Key[{}]: Type[{}]'.format(key, str(one_field.type)))
    '''
    assert len(all_fields.keys()) == 13

    receipt = {
        'contractAddress': b'contract_address',
        'status': 'CREATED',
        'ret': 'result_ret',
        'txHash': b'tx_hash',
        'feeUsed': b'fee_used',
        'cumulativeFeeUsed': b'cumulative_fee_used',
        'bloom': b'result_bloom',
        'blockNo': 10,
        'blockHash': b'block_hash',
        'txIndex': 1,
        'from': b'result_from',
        'to': b'result_to',
    }
    grpc_result2 = blockchain_pb2.Receipt(**receipt)
    tx_result2 = TxResult(grpc_result2)
    assert tx_result2.type == TxResultType.RECEIPT
    assert tx_result2.status == TxResultStatus.CREATED
    assert tx_result2.detail == receipt['ret']
    assert tx_result2.contract_address == encode_address(receipt['contractAddress'])

    grpc_result3 = blockchain_pb2.Receipt()
    grpc_result3.contractAddress = b'contract_address'
    grpc_result3.status = b'result_status'
    grpc_result3.ret = b'result_ret'
    grpc_result3.txHash = b'tx_hash'
    grpc_result3.feeUsed = b'fee_used'
    grpc_result3.cumulativeFeeUsed = b'cumulative_fee_used'
    grpc_result3.bloom = b'result_bloom'
    grpc_result3.blockNo = 10
    grpc_result3.blockHash = b'block_hash'
    grpc_result3.txIndex = 1
    #grpc_result3.from = b'result_from'
    setattr(grpc_result3, 'from', b'result_from')
    grpc_result3.to = b'result_to'
    assert len(grpc_result3.events) == 0
    events = []
    grpc_result3.events.extend(events)
    assert len(grpc_result3.events) == 0
    # TODO: add events

    assert grpc_result3.contractAddress == grpc_result2.contractAddress
    assert grpc_result3.contractAddress == receipt['contractAddress']
    assert grpc_result3.status != grpc_result2.status
    assert grpc_result3.status != receipt['status']
    assert grpc_result3.ret == grpc_result2.ret
    assert grpc_result3.ret == receipt['ret']
    assert grpc_result3.txHash == grpc_result2.txHash
    assert grpc_result3.txHash == receipt['txHash']
    assert grpc_result3.feeUsed == grpc_result2.feeUsed
    assert grpc_result3.feeUsed == receipt['feeUsed']
    assert grpc_result3.cumulativeFeeUsed == grpc_result2.cumulativeFeeUsed
    assert grpc_result3.cumulativeFeeUsed == receipt['cumulativeFeeUsed']
    assert grpc_result3.bloom == grpc_result2.bloom
    assert grpc_result3.bloom == receipt['bloom']
    assert grpc_result3.blockNo == grpc_result2.blockNo
    assert grpc_result3.blockNo == receipt['blockNo']
    assert grpc_result3.blockHash == grpc_result2.blockHash
    assert grpc_result3.blockHash == receipt['blockHash']
    assert grpc_result3.txIndex == grpc_result2.txIndex
    assert grpc_result3.txIndex == receipt['txIndex']
    #assert grpc_result3.from == grpc_result2.from
    assert getattr(grpc_result3, 'from') == getattr(grpc_result2, 'from')
    #assert grpc_result3.from == receipt['to']
    assert getattr(grpc_result3, 'from') == receipt['from']
    assert grpc_result3.to == grpc_result2.to
    assert grpc_result3.to == receipt['to']

    tx_result3 = TxResult(grpc_result3)
    assert tx_result3.type == TxResultType.RECEIPT
    assert tx_result3.status == TxResultStatus.ERROR
    assert tx_result3.detail == grpc_result3.status
    assert tx_result3.contract_address == encode_address(receipt['contractAddress'])

    grpc_result3.status = 'CREATED'
    grpc_result3.ret = 'error is occurred'
    tx_result3 = TxResult(grpc_result3)
    assert tx_result3.status != TxResultStatus.SUCCESS
    assert tx_result3.status == TxResultStatus.CREATED
    assert tx_result3.detail == 'error is occurred'

    grpc_result3.status = 'SUCCESS'
    grpc_result3.ret = 'error is occurred'
    tx_result3 = TxResult(grpc_result3)
    assert tx_result3.status == TxResultStatus.SUCCESS
    assert tx_result3.status != TxResultStatus.ERROR
    assert tx_result3.detail == grpc_result3.ret


def test_grpc_commit_result():
    grpc_result = rpc_pb2.CommitResult()
    all_fields = grpc_result.DESCRIPTOR.fields_by_name
    '''
    for key in all_fields.keys():
        one_field = all_fields[key]
        print('Key[{}]: Type[{}]'.format(key, str(one_field.type)))
    '''
    assert len(all_fields.keys()) == 3

    grpc_result.hash = b'commit_result_hash'
    grpc_result.error = rpc_pb2.TX_NONCE_TOO_LOW
    grpc_result.detail = b'commit_result_detail'

    tx_result = TxResult(grpc_result)
    assert tx_result.type == TxResultType.COMMIT_RESULT
    assert tx_result.tx_id == encode_tx_hash(b'commit_result_hash')
    assert tx_result.status == CommitStatus.TX_NONCE_TOO_LOW
    assert tx_result.detail == 'commit_result_detail'

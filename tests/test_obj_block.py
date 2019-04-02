import pytest

import decimal


from aergo.herapy.obj.block import Block
from aergo.herapy.obj.block_hash import BlockHash
from aergo.herapy.obj.transaction import TxType
from aergo.herapy.utils.encoding import encode_block_hash, decode_block_hash,\
    encode_tx_hash, decode_tx_hash, encode_payload, decode_payload,\
    encode_b58, decode_b58
from aergo.herapy.utils.converter import bigint_to_bytes, get_hash
from aergo.herapy.grpc import blockchain_pb2


def test_fail():
    with pytest.raises(TypeError):
        bh = BlockHash(1234)
        str(bh)


def test_blockhash():
    bh = BlockHash('test')
    assert bytes(bh) == decode_block_hash('test')
    assert bytes(bh) == bh.value
    assert str(bh) == 'test'

    bh = BlockHash(b'test')
    assert bytes(bh) == b'test'
    assert bytes(bh) == bh.value
    assert str(bh) == encode_block_hash(b'test')


def test_grpc_block():
    grpc_block = blockchain_pb2.Block()
    grpc_block.hash = b'block_hash'
    # header
    grpc_block.header.chainID = b'chain_id'
    grpc_block.header.prevBlockHash = b'prev_block_hash'
    grpc_block.header.blockNo = 123
    grpc_block.header.timestamp = 12345
    grpc_block.header.blocksRootHash = b'blocks_root_hash'
    grpc_block.header.txsRootHash = b'txs_root_hash'
    grpc_block.header.receiptsRootHash = b'receipts_root_hash'
    grpc_block.header.confirms = 10
    grpc_block.header.pubKey = b'pub_key'
    grpc_block.header.coinbaseAccount = b'coinbase_account'
    grpc_block.header.sign = b'block_sign'
    # body
    tx1 = blockchain_pb2.Tx()
    tx1.hash = b'tx1_hash'
    tx1.body.nonce = 10
    tx1.body.account = b'yp'
    tx1.body.recipient = b'daniel'
    tx1.body.amount = bigint_to_bytes(1)
    tx1.body.payload = b'tx1_payload'
    tx1.body.gasLimit = 1
    tx1.body.gasPrice = bigint_to_bytes(1)
    tx1.body.type = blockchain_pb2.GOVERNANCE
    tx1.body.sign = b'tx1_sign'
    tx2 = blockchain_pb2.Tx()
    tx2.hash = b'tx2_hash'
    tx2.body.nonce = 356
    tx2.body.account = b'daniel'
    tx2.body.recipient = b'hannah'
    tx2.body.amount = bigint_to_bytes(2)
    #tx2.body.payload = b'tx2_payload'
    tx2.body.gasLimit = 2
    tx2.body.gasPrice = bigint_to_bytes(2)
    tx2.body.type = blockchain_pb2.NORMAL
    tx2.body.sign = b'tx2_sign'
    grpc_block.body.txs.extend([tx1, tx2,])

    block = Block(grpc_block=grpc_block)
    assert block.hash.value == b'block_hash'
    assert block.chain_id == b'chain_id'
    assert block.height == 123
    assert block.block_no == block.height
    assert bytes(block.prev.hash) == b'prev_block_hash'
    assert block.timestamp == 12345
    assert block.blocks_root_hash == b'blocks_root_hash'
    assert block.txs_root_hash == b'txs_root_hash'
    assert block.receipts_root_hash == b'receipts_root_hash'
    assert block.confirms == 10
    assert block.public_key == b'pub_key'
    assert block.coinbase_account == b'coinbase_account'
    assert block.sign == b'block_sign'
    assert len(block.tx_list) == 2
    block_json = block.json(header_only=True)
    assert 'Body' not in block_json
    block_json = block.json(header_only=False)
    assert 'Body' in block_json
    assert 'Txs' in block_json['Body']
    assert 'Hash' in block_json
    assert block_json['Hash'] == encode_block_hash(b'block_hash')
    assert 'Header' in block_json
    assert block_json['Header']['ChainID'] == get_hash(b'chain_id', no_rand=True, no_encode=False)
    assert block_json['Header']['PreviousBlockHash'] == encode_block_hash(b'prev_block_hash')
    assert block_json['Header']['BlocksRootHash'] == encode_b58(b'blocks_root_hash')
    assert block_json['Header']['TxsRootHash'] == encode_b58(b'txs_root_hash')
    assert block_json['Header']['ReceiptsRootHash'] == encode_b58(b'receipts_root_hash')
    assert block_json['Header']['BlockNo'] == 123
    assert block_json['Header']['Timestamp'] == 12345
    assert block_json['Header']['Confirms'] == 10
    assert block_json['Header']['PubKey'] == encode_b58(b'pub_key')
    assert block_json['Header']['Sign'] == encode_b58(b'block_sign')
    assert block_json['Header']['CoinbaseAccount'] == encode_b58(b'coinbase_account')
    block_str = str(block)
    assert 'Hash' in block_str
    assert 'Header' in block_str
    assert 'Body' in block_str

    # check tx1
    block_tx1 = block.get_tx(0)
    assert block == block_tx1.block
    assert block_tx1.index_in_block == 0
    assert block_tx1.is_in_mempool == False
    assert block_tx1.nonce == 10
    block_tx1.nonce = 123
    assert block_tx1.nonce != 123
    assert block_tx1.nonce == 10
    assert bytes(block_tx1.tx_hash) == b'tx1_hash'
    assert str(block_tx1.tx_hash) == encode_tx_hash(b'tx1_hash')
    assert bytes(block_tx1.from_address) == b'yp'
    block_tx1.from_address = b'hannah'
    assert bytes(block_tx1.from_address) != b'hannah'
    assert bytes(block_tx1.from_address) == b'yp'
    assert bytes(block_tx1.to_address) == b'daniel'
    block_tx1.to_address = b'hannah'
    assert bytes(block_tx1.to_address) != b'hannah'
    assert bytes(block_tx1.to_address) == b'daniel'
    assert block_tx1.amount.aer == '1 aer'
    assert block_tx1.amount.gaer == '0.000000001 gaer'
    assert block_tx1.amount.aergo == '0.000000000000000001 aergo'
    block_tx1.amount = '100 aer'
    assert block_tx1.amount.aer != '100 aer'
    assert block_tx1.amount.aer == '1 aer'
    assert block_tx1.payload == b'tx1_payload'
    block_tx1.payload = b'new_payload'
    assert block_tx1.payload != b'new_payload'
    assert block_tx1.payload == b'tx1_payload'
    assert block_tx1.payload_str == encode_payload(b'tx1_payload')
    assert block_tx1.tx_type == TxType.GOVERNANCE
    block_tx1.tx_type = TxType.NORMAL
    assert block_tx1.tx_type != TxType.NORMAL
    assert block_tx1.tx_type == TxType.GOVERNANCE
    # check tx2
    block_tx2 = block.get_tx(1)
    assert block == block_tx2.block
    assert block_tx2.index_in_block == 1
    assert block_tx2.is_in_mempool == False
    assert block_tx2.nonce ==356
    block_tx2.nonce = 123
    assert block_tx2.nonce != 123
    assert block_tx2.nonce == 356
    assert bytes(block_tx2.tx_hash) == b'tx2_hash'
    assert str(block_tx2.tx_hash) == encode_tx_hash(b'tx2_hash')
    assert bytes(block_tx2.from_address) == b'daniel'
    block_tx2.from_address = b'yp'
    assert bytes(block_tx2.from_address) != b'yp'
    assert bytes(block_tx2.from_address) == b'daniel'
    assert bytes(block_tx2.to_address) == b'hannah'
    block_tx2.to_address = b'yp'
    assert bytes(block_tx2.to_address) != b'yp'
    assert bytes(block_tx2.to_address) == b'hannah'
    assert block_tx2.amount.aer == '2 aer'
    assert block_tx2.amount.gaer == '0.000000002 gaer'
    assert block_tx2.amount.aergo == '0.000000000000000002 aergo'
    block_tx2.amount = '100 aer'
    assert block_tx2.amount.aer != '100 aer'
    assert block_tx2.amount.aer == '2 aer'
    assert block_tx2.payload == b''
    block_tx2.payload = b'new_payload'
    assert block_tx2.payload != b'new_payload'
    assert block_tx2.payload == b''
    assert block_tx2.payload_str == None
    assert block_tx2.tx_type == TxType.NORMAL
    block_tx2.tx_type = TxType.GOVERNANCE
    assert block_tx2.tx_type != TxType.GOVERNANCE
    assert block_tx2.tx_type == TxType.NORMAL

def test_block():
    bh = BlockHash('test')

import json
from aergo.herapy.utils.converter import (
    convert_bytes_to_hex_str,
    convert_bytes_to_int_str,
)


def test_blockchain(aergo) -> None:
    print("------ Get Node Info -----------")
    node_state = aergo.get_node_state()
    print("Node State: {}".format(str(node_state)))
    node_info = aergo.get_node_info()
    print("Node Info: {}".format(str(node_info)))

    print("------ Get Blockchain Info -----------")
    blockchain_info = aergo.get_chain_info()
    print("Blockchain Info: {}".format(str(blockchain_info)))
    blockchain_info = aergo.get_chain_info(with_consensus_info=False)
    print("Blockchain Info: {}".format(str(blockchain_info)))

    print("------ Get Consensus Info -----------")
    consensus_info = aergo.get_consensus_info()
    print("Consensus Info: {}".format(str(consensus_info)))

    print("------ Get Blockchain Status -----------")
    blockchain_status = aergo.get_status()
    print("Blockchain Status: {}".format(str(blockchain_status)))
    print("Best Block Hash      = {}"
          .format(str(blockchain_status.best_block_hash)))
    print("Best Block Height    = {}"
          .format(blockchain_status.best_block_height))
    print("Best Chain ID Hash         = {}"
          .format(blockchain_status.best_chain_id_hash))
    print("base58(Best Chain ID Hash) = {}"
          .format(blockchain_status.best_chain_id_hash_b58))
    consensus_info = blockchain_status.consensus_info
    print("Consensus Info       = {}".format(consensus_info))
    print("Consensus Info: type     = {}".format(consensus_info.type))
    print("Consensus Info: status   = {}".format(consensus_info.status))
    print("Consensus Info: LIB hash = {}".format(consensus_info.lib_hash))
    print("Consensus Info: LIB no   = {}".format(consensus_info.lib_no))

    best_block_hash, best_block_height = aergo.get_blockchain_status()
    print("Best Block Hash      = {}".format(best_block_hash))
    print("str(Best Block Hash)     = {}".format(str(best_block_hash)))
    print("bytes(Best Block Hash)   = {!r}".format(bytes(best_block_hash)))
    print("int(Best Block Hash)     = {}"
          .format(convert_bytes_to_int_str(bytes(best_block_hash))))
    print("hex(Best Block Hash)     = {}"
          .format(convert_bytes_to_hex_str(bytes(best_block_hash))))
    print("Best Block Height    = {}".format(best_block_height))

    print("------ Get Blockchain Headers -----------")
    block_headers = aergo.get_block_headers(
        block_height=best_block_height, offset=best_block_height - 1)
    for i, b in enumerate(block_headers):
        print('[{}] block: {}'.format(i, str(b)))

    print("------ Get Blockchain metas -----------")
    block_metas = aergo.get_block_metas(
        block_height=best_block_height, offset=best_block_height - 1)
    for i, b in enumerate(block_metas):
        print('[{}] block: {}'
              .format(i, json.dumps(b.json(header_only=True), indent=2)))
    block_meta = aergo.get_block_meta(block_height=1)
    print("Block meta: ", block_meta)

    print("------ Get Block Status -----------")
    block = aergo.get_block(best_block_hash)
    print("Block Chain ID Hash         = ", block.chain_id_hash)
    print("base58(Block Chain ID Hash) = ", block.chain_id_hash_b58)
    print("Block Hash = ", block.hash)
    print("  Height = ", block.height)
    print("  Timestamp = ", block.timestamp)
    print("  Blocks Root Hash = ", block.blocks_root_hash)
    print("  Txs Root Hash = ", block.txs_root_hash)
    print("  Confirm = ", block.confirms)
    print("  Pub Key = ", block.public_key)
    print("  Sign = ", block.sign)
    print("  previous block hash =\n{}".format(block.prev))
    print("  Txs = ", block.tx_list)
    print(json.dumps(block.json(), indent=2))

    block = aergo.get_block(block_height=best_block_height)
    print(block)
    print("Block Hash = ", block.hash)
    print("  Height = ", block.height)
    print("  Timestamp = ", block.timestamp)
    print("  Blocks Root Hash = ", block.blocks_root_hash)
    print("  Txs Root Hash = ", block.txs_root_hash)
    print("  Confirm = ", block.confirms)
    print("  Pub Key = ", block.public_key)
    print("  Sign = ", block.sign)
    print("  previous block hash =\n{}".format(block.prev))
    print("  Txs = ", block.tx_list)

    print("------ Get Peers -----------")
    # definition of peer needs to describe.
    peers = aergo.get_peers()
    for p in peers:
        print(p)

    print("------ Get Node State -----------")
    node_state = aergo.get_node_state()
    print(node_state)
    node_state_fmt_txt = json.dumps(node_state, indent=2, sort_keys=True)
    print(node_state_fmt_txt)

import sys
import traceback
import json

import aergo.herapy as herapy
from aergo.herapy.utils.converter import convert_bytes_to_hex_str, \
                                         convert_bytes_to_int_str


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Blockchain Status -----------")
        best_block_hash, best_block_height = aergo.get_blockchain_status()
        print("Best Block Hash      = {}".format(best_block_hash))
        print("str(Best Block Hash)     = {}".format(str(best_block_hash)))
        print("bytes(Best Block Hash)   = {}".format(bytes(best_block_hash)))
        print("int(Best Block Hash)     = {}"
              .format(convert_bytes_to_int_str(bytes(best_block_hash))))
        print("hex(Best Block Hash)     = {}"
              .format(convert_bytes_to_hex_str(bytes(best_block_hash))))
        print("Best Block Height    = {}".format(best_block_height))

        print("------ Get Block Status -----------")
        block = aergo.get_block(best_block_hash)
        print(json.dumps(block.json(), indent=2))
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

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

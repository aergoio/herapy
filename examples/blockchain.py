import grpc
import json

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Blockchain Status -----------")
        best_block_hash, best_block_height = aergo.get_blockchain_status()
        print("Best Block Hash      = {}".format(best_block_hash))
        print("Best Block Height    = {}".format(best_block_height))

        print("------ Get Block Status -----------")
        block = aergo.get_block(best_block_hash)
        print("Block Hash = ", block.hash)
        print("  Height = ", block.height)
        print("  Timestamp = ", block.timestamp)
        print("  Root Hash = ", block.blocks_root_hash)
        print("  Txs Root Hash = ", block.txs_root_hash)
        print("  Confirm = ", block.confirms)
        print("  Pub Key = ", block.public_key)
        print("  Sign = ", block.sign)
        print("  previous block hash = ", block.prev.hash)
        print("  Body = ", block.body)

        block = aergo.get_block(block_height=best_block_height)
        print("Block Hash = ", block.hash)
        print("  Height = ", block.height)
        print("  Timestamp = ", block.timestamp)
        print("  Root Hash = ", block.blocks_root_hash)
        print("  Txs Root Hash = ", block.txs_root_hash)
        print("  Confirm = ", block.confirms)
        print("  Pub Key = ", block.public_key)
        print("  Sign = ", block.sign)
        print("  previous block hash = ", block.prev.hash)
        print("  Body = ", block.body)

        print("------ Get Peers -----------")
        peers = aergo.get_peers()
        print(peers)

        print("------ Get Node State -----------")
        node_state = aergo.get_node_state()
        print(node_state)
        node_state_fmt_txt = json.dumps(node_state, indent=2, sort_keys=True)
        print(node_state_fmt_txt)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        # TODO exception handling using AERGO
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

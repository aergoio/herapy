import grpc
import json

import herapy


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
        print(block.info)

        block = aergo.get_block(block_height=best_block_height)
        print(block.info)

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
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

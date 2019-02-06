import sys
import traceback
import json

import aergo.herapy as herapy
from aergo.herapy.utils.converter import convert_bytes_to_hex_str, \
                                         convert_bytes_to_int_str


def run():
    try:
        aergo1 = herapy.Aergo()
        aergo2 = herapy.Aergo()
        aergo3 = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo1.connect('localhost:17801')
        aergo2.connect('localhost:17802')
        aergo3.connect('localhost:17803')

        print("------ Get Blockchain Status -----------")
        best_block_hash, best_block_height = aergo1.get_blockchain_status()
        print("(aergo1) Best Block Hash      = {}".format(best_block_hash))
        print("(aergo1) Best Block Height    = {}".format(best_block_height))

        best_block_hash, best_block_height = aergo2.get_blockchain_status()
        print("(aergo2) Best Block Hash      = {}".format(best_block_hash))
        print("(aergo2) Best Block Height    = {}".format(best_block_height))

        best_block_hash, best_block_height = aergo3.get_blockchain_status()
        print("(aergo3) Best Block Hash      = {}".format(best_block_hash))
        print("(aergo3) Best Block Height    = {}".format(best_block_height))

        print("------ Get Block Status -----------")
        block = aergo1.get_block(block_height=best_block_height)
        print("Aergo 1:\n{}".format(json.dumps(block.json(), indent=2)))

        aergo1.disconnect()
        aergo2.disconnect()
        aergo3.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

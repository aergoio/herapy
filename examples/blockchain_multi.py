import sys
import traceback
import json

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    try:
        aergo1 = herapy.Aergo()
        aergo2 = herapy.Aergo()
        aergo3 = herapy.Aergo()
        aergo4 = herapy.Aergo()

        print("------ Connect AERGO -----------")
        """
        aergo1.connect('localhost:17801')
        aergo2.connect('localhost:17802')
        aergo3.connect('localhost:17803')
        """
        aergo1.connect('ec2-52-56-86-84.eu-west-2.compute.amazonaws.com:17845')
        aergo2.connect('ec2-13-57-31-165.us-west-1.compute.amazonaws.com:17845')
        aergo3.connect('ec2-3-86-18-207.compute-1.amazonaws.com:17845')
        aergo4.connect('ec2-54-180-100-160.ap-northeast-2.compute.amazonaws.com:17845')

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

        best_block_hash, best_block_height = aergo4.get_blockchain_status()
        print("(aergo4) Best Block Hash      = {}".format(best_block_hash))
        print("(aergo4) Best Block Height    = {}".format(best_block_height))

        print("------ Get Block Status -----------")
        best_block_height = best_block_height - 2
        block1 = aergo1.get_block(block_height=best_block_height)
        print("Aergo 1:\n{}".format(str(block1.hash)))
        block2 = aergo2.get_block(block_height=best_block_height)
        print("Aergo 2:\n{}".format(str(block2.hash)))
        block3 = aergo3.get_block(block_height=best_block_height)
        print("Aergo 3:\n{}".format(str(block3.hash)))
        block4 = aergo4.get_block(block_height=best_block_height)
        print("Aergo 4:\n{}".format(str(block4.hash)))

        aergo1.disconnect()
        aergo2.disconnect()
        aergo3.disconnect()
        aergo4.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

import grpc
import base58

from herapy.comm.comm import Comm


def get_blockchain_status(comm):
    status = comm.get_blockchain_status()
    print('Return Msg: %s' % comm.get_result_to_json())
    return status.best_block_hash, status.best_height


def get_block_headers(comm, height):
    list = comm.get_block_headers(height=height, size=3)
    print('Return Msg: %s' % comm.get_result_to_json())
    return list


def get_block(comm, hash, height=0):
    block = comm.get_block(block_hash=hash, block_height=height)
    print('Return Msg: %s' % comm.get_result_to_json())
    return block


def run():
    try:
        comm = Comm('localhost:7845')
        print("------ Get Blockchain Status -----------")
        best_block_hash, best_height = get_blockchain_status(comm)
        print('  - Best Block Hash  : %s' % base58.b58encode_check(best_block_hash))
        print('  - Best Block Height: %s' % best_height)

        print("------ Get Best Block -----------")
        block = get_block(comm, None, best_height)
        print('Best Block = %s' % block.SerializeToString())

        print("------ Get Blocks -----------")
        result = get_block_headers(comm, best_height)
        print('Block Headers = %s' % result.SerializeToString())
        if result.blocks[0].hash != best_block_hash:
            print("SOMETHING WRONG!!!!!!")
            return

        size = len(result.blocks)
        for idx in range(size):
            print("  [%s]" % idx)
            print("  - Hash           : %s" % result.blocks[idx].hash)
            print("  - Hash with sha  : %s" % base58.b58encode_check(result.blocks[idx].hash))
            print("  - Hash no sha    : %s" % base58.b58encode(result.blocks[idx].hash))
            header = result.blocks[idx].header
            print("  - Header")
            print("    - Previous Block Hash : %s" % base58.b58encode_check(header.prevBlockHash))
            print("    - Block Number        : %s" % header.blockNo)
            print("    - Timestamp           : %s" % header.timestamp)
            print("    - Txs Root Hash       : %s" % base58.b58encode_check(header.txsRootHash))
            print("    - Confirmed           : %s" % (header.confirms == 1))
            print("    - Public Key          : %s" % base58.b58encode_check(header.pubKey))
            print("    - Sign                : %s" % base58.b58encode_check(header.sign))

            block = get_block(comm, result.blocks[idx].hash)
            print('  - Block = %s' % block.SerializeToString())
            print("    - Body : %s" % block.body)
    except grpc.RpcError as e:
        print('Get Blockchain Info failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

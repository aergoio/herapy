import grpc

from herapy.comm.comm import Comm


def get_blockchain_status(comm):
    status = comm.get_blockchain_status()
    print('Return Msg: %s' % comm.get_result_to_json())
    return status


def run():
    try:
        print("------ Get Blockchain Status -----------")
        comm = Comm('localhost:7845')
        result = get_blockchain_status(comm)
        print('Blockchain Status = %s' % result.SerializeToString())
        print('  - Best Block Hash  : %s' % result.best_block_hash.hex())
        print('  - Best Block Height: %s' % result.best_height)
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

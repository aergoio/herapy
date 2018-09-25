import grpc
import base58

from herapy.comm.comm import Comm


def get_node_state(comm, timeout):
    status = comm.get_node_state(timeout)
    print('Return Msg: %s' % comm.get_result_to_json())
    return status


def run():
    try:
        print("------ Get Node State -----------")
        comm = Comm('localhost:10001')
        timeout = 3
        node_state = get_node_state(comm, timeout)
        print('Node State = %s' % node_state.SerializeToString())
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

import grpc
import base58

from herapy.comm.comm import Comm


def get_peers(comm):
    status = comm.get_peers()
    print('Return Msg: %s' % comm.get_result_to_json())
    return status


def run():
    try:
        print("------ Get Peers -----------")
        comm = Comm('localhost:7845')
        peer_list = get_peers(comm)
        print('Peers = %s' % peer_list.SerializeToString())

        num_peer = len(peer_list.peers)
        print('Number of Peer: %s' % num_peer)

        if num_peer > 0:
            for idx in range(num_peer):
                peer = peer_list.peers[idx]
                state = peer_list.states[idx]
                print("Peer[%s]'s state: %s" % (idx, state))
                print("  - ID     : %s" % base58.b58encode_check(peer.peerID))
                print("  - address: %s" % base58.b58encode_check(peer.address))
                print("  - port   : %s" % peer.port)
        else:
            print("NO Peer!")
    except grpc.RpcError as e:
        print('Get Peers failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

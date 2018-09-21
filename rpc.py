import grpc

# TODO: refactor these to use package imports when grpc working
import rpc_pb2
import rpc_pb2_grpc

class Rpc:
    def __init__(self, channel):
        channel = grpc.insecure_channel(channel)
        self.rpc = rpc_pb2_grpc.AergoRPCServiceStub(channel)
        self.empty = rpc_pb2.Empty()

    # Accounts
    

    def node_state(self):
        return self.rpc.NodeState(rpc_pb2.SingleBytes())

    def blockchain(self):
        return self.rpc.Blockchain(self.empty)

    def list_block_headers(self):


    def get_accounts(self):
        return self.rpc.GetAccounts(self.empty)

    def get_peers(self):
        return self.rpc.GetPeers(self.empty)

    def create_account(self):
        return self.rpc.CreateAccount()


rpc = Rpc('localhost:7845')
print(rpc.get_accounts())
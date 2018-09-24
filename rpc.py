import grpc
import base58

# TODO: refactor these to use package imports when grpc working
import rpc_pb2
import rpc_pb2_grpc

from herapy.utils.encoding import encode_address

class Rpc:
    def __init__(self, channel):
        channel = grpc.insecure_channel(channel)
        self.rpc = rpc_pb2_grpc.AergoRPCServiceStub(channel)
        self.empty = rpc_pb2.Empty()

    # Accounts
    def create_account(self, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        account = self.rpc.CreateAccount(personal)
        return encode_address(account)

    def get_accounts(self):
        accounts = self.rpc.GetAccounts(self.empty).accounts
        addresses = [ encode_address(account.address) for account in accounts ]
        return addresses

    def node_state(self):
        return self.rpc.NodeState(rpc_pb2.SingleBytes())

    def blockchain(self):
        return self.rpc.Blockchain(self.empty)

    def list_block_headers(self):
        pass

    def get_peers(self):
        return self.rpc.GetPeers(self.empty)

rpc = Rpc('localhost:7845')
for account in rpc.get_accounts():
    print(account)
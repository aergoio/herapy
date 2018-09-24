import grpc
import base58

from herapy.grpc import rpc_pb2
from herapy.grpc import rpc_pb2_grpc
from herapy.grpc import blockchain_pb2


def create_account(rpc_stub):
    person = rpc_pb2.Personal()
    person.passphrase = 'password'
    account = rpc_stub.CreateAccount(person)
    return account


def get_account_state(rpc_stub, account):
    account_state = rpc_stub.GetState(account)
    return account_state


def run():
    with grpc.insecure_channel('localhost:7845') as channel:
        rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(channel)

        print("------ Create Account -----------")
        account = create_account(rpc_stub)
        print('New Account Address = %s\n' % base58.b58encode(account.address))

        print("------ Get Account State -----------")
        account_state = get_account_state(rpc_stub, account)
        print('  - Nonce:        %s' % account_state.nonce)
        print('  - Balance:      %s' % account_state.balance)
        print('  - Code Hash:    %s' % account_state.codeHash)
        print('  - Storage Root: %s' % account_state.storageRoot)

if __name__ == '__main__':
    run()

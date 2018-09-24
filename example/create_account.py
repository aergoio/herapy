import grpc
import base58

from herapy.comm.comm import Comm


def create_account(comm, passphrase):
    account = comm.create_account(passphrase)
    print('Return Msg: %s' % comm.get_result_to_json())
    return account


def get_account_state(comm, account):
    state = comm.get_account_state(account)
    print('Return Msg: %s' % comm.get_result_to_json())
    return state


def run():
    try:
        comm = Comm('localhost:7845')
        print("------ Create Account -----------")
        account = create_account(comm, 'password')
        print('New Account Address = %s\n' % base58.b58encode(account.address))

        print("------ Get Account State -----------")
        account_state = get_account_state(comm, account)
        print('  - Nonce:        %s' % account_state.nonce)
        print('  - Balance:      %s' % account_state.balance)
        print('  - Code Hash:    %s' % account_state.codeHash)
        print('  - Storage Root: %s' % account_state.storageRoot)
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

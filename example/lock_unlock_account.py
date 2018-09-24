import grpc
import base58

from herapy.comm.comm import Comm


def create_account(comm, passphrase):
    account = comm.create_account(passphrase)
    print('Return Msg: %s' % comm.get_result_to_json())
    return account


def get_account_state(comm, address):
    state = comm.get_account_state_from_b58address(address)
    print('Return Msg: %s' % comm.get_result_to_json())
    return state


def lock_account(comm, address, passphrase):
    account = comm.lock_account_from_b58address(address, passphrase)
    print('Return Msg: %s' % comm.get_result_to_json())
    return account


def unlock_account(comm, address, passphrase):
    account = comm.unlock_account_from_b58address(address, passphrase)
    print('Return Msg: %s' % comm.get_result_to_json())
    return account


def run():
    try:
        passphrase = 'password'
        comm = Comm('localhost:7845')
        print("------ Create Account -----------")
        account = create_account(comm, passphrase)
        address = base58.b58encode_check(account.address)
        #address = 'CYBquT7VWgjXaXZvsMnNCbjQYptiWvfVPxmDxJfF9dGqg'
        print('New Account Address = %s\n' % address)

        print("------ Lock Account -----------")
        ret_acc = lock_account(comm, address, passphrase)
        print("Lock Account's address: %s" % base58.b58encode_check(ret_acc.address))

        print("------ Get Account State -----------")
        account_state = get_account_state(comm, address)
        print("Account[%s] State: " % address)
        print('  - Nonce:        %s' % account_state.nonce)
        print('  - Balance:      %s' % account_state.balance)
        print('  - Code Hash:    %s' % account_state.codeHash)
        print('  - Storage Root: %s' % account_state.storageRoot)

        print("------ Unlock Account -----------")
        ret_acc = unlock_account(comm, address, passphrase)
        print("Unlock Account's address: %s" % base58.b58encode_check(ret_acc.address))

        print("------ Get Account State -----------")
        account_state = get_account_state(comm, address)
        print("Account[%s] State: " % address)
        print('  - Nonce:        %s' % account_state.nonce)
        print('  - Balance:      %s' % account_state.balance)
        print('  - Code Hash:    %s' % account_state.codeHash)
        print('  - Storage Root: %s' % account_state.storageRoot)

    except grpc.RpcError as e:
        print('Get Accounts failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

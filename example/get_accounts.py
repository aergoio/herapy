import grpc
import base58

from herapy.comm.comm import Comm

def get_accounts(comm):
    account_list = comm.get_accounts()
    print('Return Msg: %s' % comm.get_result_to_json())
    return account_list


def run():
    try:
        comm = Comm('localhost:7845')
        print("------ Get Accounts -----------")
        account_list = get_accounts(comm)
        print("Account List is %s" % account_list.SerializeToString())

        num_acc = len(account_list.accounts)
        print('Number of Account: %s' % num_acc)

        if num_acc > 0:
            for idx in range(num_acc):
                account = account_list.accounts[idx]
                address = base58.b58encode(account.address)
                print("Account[%s]'s address = %s" % (idx, address))

    except grpc.RpcError as e:
        print('Get Accounts failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

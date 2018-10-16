import grpc
import base58

import herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Accounts -----------")
        accounts = aergo.get_all_accounts()
        i = 0
        for acc in accounts:
            i += 1
            print('Account[%s] address: %s' % (i, acc.address_str))
        '''
        print('  - Nonce:        %s' % result.nonce)
        print('  - Balance:      %s' % result.balance)
        print('  - Code Hash:    %s' % result.codeHash)
        print('  - Storage Root: %s' % result.storageRoot)
        '''

        print("------ Create Account -----------")
        password = "test password"
        account = aergo.create_account(password=password)

        print("Private Key      = {}".format(account.private_key))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))
        print("Address String   = {}".format(account.address_str))

        print("------ Get Account State -----------")
        result = aergo.get_account_state(account)
        print('Return Msg: %s' % result)
        '''
        print('  - Nonce:        %s' % result.nonce)
        print('  - Balance:      %s' % result.balance)
        print('  - Code Hash:    %s' % result.codeHash)
        print('  - Storage Root: %s' % result.storageRoot)
        '''

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

import grpc

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Accounts without State in Node -----------")
        accounts = aergo.get_node_accounts(skip_state=True)
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance        = {}".format(account.balance))
            print("    - nonce          = {}".format(account.nonce))
            print("    - code hash      = {}".format(account.code_hash))
            print("    - storage root   = {}".format(account.storage_root))

        print("------ Get Accounts in Node -----------")
        accounts = aergo.get_node_accounts()
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance        = {}".format(account.balance))
            print("    - nonce          = {}".format(account.nonce))
            print("    - code hash      = {}".format(account.code_hash))
            print("    - storage root   = {}".format(account.storage_root))

        print("------ Create Account -----------")
        password = "test password"
        account = aergo.new_account(password=password)

        print("Private Key      = {}".format(account.private_key))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))

        print("------ Get Account State -----------")
        aergo.get_account()
        print("  > account state in 'aergo'")
        print('    - Nonce:        %s' % aergo.account.nonce)
        print('    - Balance:      %s' % aergo.account.balance)
        print('    - Code Hash:    %s' % aergo.account.code_hash)
        print('    - Storage Root: %s' % aergo.account.storage_root)

        print("------ Get Configured Account -----------")
        conf_keys_str = """
1:6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW:AmPESicKLcPYXJC7ufgK6ti3fVS1r1SbqfxhVDEnTUc5cPXT1474
"""
        conf_keys_line = conf_keys_str.split('\n')
        conf_keys = []
        for l in conf_keys_line:
            if 0 == len(l):
                continue
            conf_keys.append(l.split(':'))
        print("  - Configured Keys:\n{}".format(conf_keys))

        for k in conf_keys:
            print("  [{}]".format(k[0]))
            print("    > private key   : {}".format(k[1]))
            print("    > address       : {}".format(k[2]))

            # check account state
            a = aergo.get_account(k[2])
            print("    > account state : {}".format(a))
            print("      - balance        = {}".format(a.balance))
            print("      - nonce          = {}".format(a.nonce))
            print("      - code hash      = {}".format(a.code_hash))
            print("      - storage root   = {}".format(a.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

import grpc

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Accounts in Node -----------")
        accounts = aergo.get_node_accounts()
        for i in range(len(accounts)):
            print("Account[{0}]'s address in Node is {1}".format(i, accounts[i].address_str))
            state = aergo.get_account_state(accounts[i])
            print("  > account state : {}".format(state))
            print("    - balance        = {}".format(accounts[i].balance))
            print("    - nonce          = {}".format(accounts[i].nonce))
            print("    - code hash      = {}".format(accounts[i].code_hash))
            print("    - storage root   = {}".format(accounts[i].storage_root))

        print("------ Create Account -----------")
        password = "test password"
        account = aergo.new_account(password=password)

        print("Private Key      = {}".format(account.private_key))
        print("str(Private Key) = {}".format(account.private_key_str))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))
        print("str(Address)     = {}".format(account.address_str))

        print("------ Get Account State -----------")
        state = aergo.get_account_state()
        print("  > account state : {}".format(state))
        print('    - Nonce:        %s' % account.nonce)
        print('    - Balance:      %s' % account.balance)
        print('    - Code Hash:    %s' % account.code_hash)
        print('    - Storage Root: %s' % account.storage_root)

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
            a = herapy.Account("", empty=True)
            a.address = k[2]
            state = aergo.get_account_state(a)
            print("    > account state : {}".format(state))
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

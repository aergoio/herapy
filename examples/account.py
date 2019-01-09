import sys
import traceback

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('testnet.aergo.io:7845')

        print("------ Get Accounts without State in Node -----------")
        accounts = aergo.get_node_accounts(skip_state=True)
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo      = {}".format(account.balance.aergo))
            print("        + gaer       = {}".format(account.balance.gaer))
            print("        + aer        = {}".format(account.balance.aer))
            print("    - nonce          = {}".format(account.nonce))
            print("    - code hash      = {}".format(account.code_hash))
            print("    - storage root   = {}".format(account.storage_root))

        print("------ Get Accounts in Node -----------")
        accounts = aergo.get_node_accounts()
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo      = {}".format(account.balance.aergo))
            print("        + gaer       = {}".format(account.balance.gaer))
            print("        + aer        = {}".format(account.balance.aer))
            print("    - nonce          = {}".format(account.nonce))
            print("    - code hash      = {}".format(account.code_hash))
            print("    - storage root   = {}".format(account.storage_root))

        print("------ Create Account -----------")
        password = "test password"
        account = aergo.new_account()

        print("Private Key      = {}".format(account.private_key))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))

        print("------ Get Account State -----------")
        aergo.get_account()
        print("  > account state in 'aergo'")
        print('    - Nonce:        %s' % aergo.account.nonce)
        print("    - balance")
        print("        + aergo      = {}".format(aergo.account.balance.aergo))
        print("        + gaer       = {}".format(aergo.account.balance.gaer))
        print("        + aer        = {}".format(aergo.account.balance.aer))
        print('    - Code Hash:    %s' % aergo.account.code_hash)
        print('    - Storage Root: %s' % aergo.account.storage_root)
        print(account)

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
            a = aergo.get_account(address=k[2])
            print("    > account state : {}".format(a))
            print("      - balance        = {}".format(a.balance))
            print("        + aergo          = {}".format(aergo.account.balance.aergo))
            print("        + gaer           = {}".format(aergo.account.balance.gaer))
            print("        + aer            = {}".format(aergo.account.balance.aer))
            print("      - nonce          = {}".format(a.nonce))
            print("      - code hash      = {}".format(a.code_hash))
            print("      - storage root   = {}".format(a.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

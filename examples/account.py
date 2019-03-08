import sys
import traceback

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Accounts without State in Node -----------")
        accounts = aergo.get_node_accounts(skip_state=True)
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo              = {}".format(account.balance.aergo))
            print("        + gaer               = {}".format(account.balance.gaer))
            print("        + aer                = {}".format(account.balance.aer))
            print("    - nonce                  = {}".format(account.nonce))
            print("    - code hash              = {}".format(account.code_hash))
            print("    - storage root           = {}".format(account.storage_root))
            print("    - sql recovery point     = {}".format(account.sql_recovery_point))

        print("------ Get Accounts in Node -----------")
        accounts = aergo.get_node_accounts()
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo              = {}".format(account.balance.aergo))
            print("        + gaer               = {}".format(account.balance.gaer))
            print("        + aer                = {}".format(account.balance.aer))
            print("    - nonce                  = {}".format(account.nonce))
            print("    - code hash              = {}".format(account.code_hash))
            print("    - storage root           = {}".format(account.storage_root))
            print("    - sql recovery point     = {}".format(account.sql_recovery_point))

        print("------ Create Account -----------")
        account = aergo.new_account()

        print("Private Key      = {}".format(account.private_key))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))

        print("------ Get Account State -----------")
        aergo.get_account()
        print("  > account state in 'aergo'")
        print("    - balance")
        print("        + aergo              = {}".format(account.balance.aergo))
        print("        + gaer               = {}".format(account.balance.gaer))
        print("        + aer                = {}".format(account.balance.aer))
        print("    - nonce                  = {}".format(account.nonce))
        print("    - code hash              = {}".format(account.code_hash))
        print("    - storage root           = {}".format(account.storage_root))
        print("    - sql recovery point     = {}".format(account.sql_recovery_point))
        print(account)

        print("------ Get Configured Account -----------")
        accounts = [
            {
                "private_key": "eHoEcHnaxpGpgzknXjuwon8VFVrLkKHC4FckGuGkQ8depiDDfyUAWC3L",
                "address": "AmPZKCJpT98V9Tc8dBUbRg78M1jgoB1ZEh97Rs1r5KewPcCiURf7",
            },
        ]
        for i, account in enumerate(accounts):
            print("  [{}]".format(i))
            print("    > private key   : {}".format(account['private_key']))
            print("    > address       : {}".format(account['address']))

            # check account state
            a = aergo.get_account(address=account['address'])
            print("    > account state : {}".format(a))
            print("    - balance")
            print("        + aergo              = {}".format(a.balance.aergo))
            print("        + gaer               = {}".format(a.balance.gaer))
            print("        + aer                = {}".format(a.balance.aer))
            print("    - nonce                  = {}".format(a.nonce))
            print("    - code hash              = {}".format(a.code_hash))
            print("    - storage root           = {}".format(a.storage_root))
            print("    - sql recovery point     = {}".format(a.sql_recovery_point))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

import grpc

import herapy


def run():
    try:
        aergo = herapy.Aergo()
        exported_txt = "485ccQXjmT3JeUHV16n16LzAJhhfHHkv9HU9k7c5PeJDyPMAdLcCu8Yqws19UzMP4K4Rq2MkQ"

        print("------ Import Account -----------")
        account = aergo.import_account(exported_txt, password='1234')
        print("Account private key is {}".format(account.private_key_str))
        print("Account address is {}".format(account.address_str))

        print("------ Export Account -----------")
        new_exp_txt = aergo.export_account(account)
        print("Exported txt is {}".format(new_exp_txt))

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Account State -----------")
        state = aergo.get_account_state(account)
        print("  > account state : {}".format(state))
        print("    - balance        = {}".format(account.balance))
        print("    - nonce          = {}".format(account.nonce))
        print("    - code hash      = {}".format(account.code_hash))
        print("    - storage root   = {}".format(account.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

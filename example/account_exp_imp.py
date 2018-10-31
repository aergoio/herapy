import grpc

import herapy


def run():
    try:
        aergo = herapy.Aergo()
        exported_txt = "47DxggYTgyv7g5dYnGXDniFR1dRH7xr88eRwZH9dFCBWQ8qVyjhybeB3QKdNPstPYr5NqyfZd"
        address = "AmQ8pMdRNvgC47re3oJnFstn9pKhWEmFoWjvo9aEE5MsTFHpKewf"

        print("------ Import Account -----------")
        account = aergo.import_account(exported_txt, password='1234')
        print("Account address is {}".format(account.address_str))

        print("------ Export Account -----------")
        new_exp_txt = aergo.export_account(account)
        print("Exported txt is {}".format(new_exp_txt))

        print("------ Connect AERGO -----------")
        aergo.connect('184.99.19.240:7845')
        #aergo.connect('localhost:7845')

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

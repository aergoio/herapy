import sys
import traceback

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Export New Account -----------")
        aergo.new_account()
        new_exp_txt = aergo.export_account(password="1234")
        print("Exported txt is {}".format(new_exp_txt))

        print("------ Import Account -----------")
        try:
            aergo.import_account(new_exp_txt, password='test')
        except herapy.errors.GeneralException:
            print("It should be failed.")

        print("------ Import Account -----------")
        try:
            account = aergo.import_account(new_exp_txt, password='1234')
            print("Account private key is {}".format(account.private_key))
            print("Account address is {}".format(account.address))
        except herapy.errors.GeneralException:
            print("It should be failed.")

        print("------ Import Account -----------")
        exported_txt = "485ccQXjmT3JeUHV16n16LzAJhhfHHkv9HU9k7c5PeJDyPMAdLcCu8Yqws19UzMP4K4Rq2MkQ"
        account = aergo.import_account(exported_txt, password='1234')
        print("Account private key is {}".format(account.private_key))
        print("Account address is {}".format(account.address))

        print("------ Export Account -----------")
        new_exp_txt = aergo.export_account(password='1234')
        print("Exported txt is {}".format(new_exp_txt))

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Account State -----------")
        a = aergo.get_account(address=account.address)
        print("  > account state of Import account")
        print("    - balance        = {}".format(a.balance))
        print("    - nonce          = {}".format(a.nonce))
        print("    - code hash      = {}".format(a.code_hash))
        print("    - storage root   = {}".format(a.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

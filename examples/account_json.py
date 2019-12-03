import sys
import traceback
import time
import json

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    try:
        print("------ Set Sender Account -----------")
        sender_json = '{"address": "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad", "enc_key": "47QHSuhBTZ4b7nbw2zJz5EARyQ4XS8gDxhFDeu5mYeKNqfHhwRutUmja3WRxV1suB12eWBeDZ"}'
        sender_account = herapy.Account.from_json(sender_json, password='5678')
        print("  > Sender Account before connecting: {}".format(sender_account))
        print("     > address:     {}".format(sender_account.address))
        print("     > private key: {}".format(sender_account.private_key))

        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Set Sender Account -----------")
        aergo.account = sender_account
        aergo.get_account()
        print("  > Sender Account after connecting: {}".format(aergo.account))

        print("------ Set Receiver Account -----------")
        receiver_json = '{"address": "AmMPQqRJ4pd8bS9xdkw5pjExtLjaUXaYGB5kagzHu4A9ckKgnBV2"}'
        receiver_account = herapy.Account.from_json(receiver_json)
        receiver_account = aergo.get_account(account=receiver_account)
        print("  > Receiver Account: {}".format(receiver_account))

        print("------ Simple Transfer -----------")
        simple_tx, result = aergo.transfer(to_address=receiver_account.address,
                                           amount=10000000000)
        print("  > simple TX[{}]".format(simple_tx.calculate_hash()))
        print("{}".format(str(simple_tx)))
        print("  > result: ", result)
        if result.status != herapy.CommitStatus.TX_OK:
            eprint("    > ERROR[{0}]: {1}".format(result.status, result.detail))
            aergo.disconnect()
            return
        else:
            print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))

        print("------ Check Account Info #1 -----------")
        aergo.get_account()
        print("  > Sender Account: {}".format(aergo.account))
        receiver_account = aergo.get_account(receiver_account)
        print("  > Receiver Account: {}".format(receiver_account))

        time.sleep(3)

        print("------ Check Account Info #2 -----------")
        aergo.get_account()
        print("  > Sender Account: {}".format(aergo.account))
        receiver_account = aergo.get_account(receiver_account)
        print("  > Receiver Account: {}".format(receiver_account))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

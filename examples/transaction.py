import sys
import traceback
import time

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('testnet.aergo.io:7845')

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address))
        aergo.get_account()
        print("    > account state of Sender")
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Set Receiver Account -----------")
        receiver_address = "AmNHbk46L5ZaFH942mxDrunhUb34S8xRd7ygNnqaW5nqJDt5ugKD"
        print("  > Receiver Address: {}".format(receiver_address))

        print("------ Simple Send Tx -----------")
        simple_tx, result = aergo.send_payload(to_address=receiver_address,
                                               amount=10, payload=None,
                                               retry_nonce=3)
        print("  > simple TX[{}]".format(simple_tx.calculate_hash()))
        print("{}".format(herapy.utils.convert_tx_to_formatted_json(simple_tx)))
        print("      result: ", result)
        if result.status != herapy.CommitStatus.TX_OK:
            eprint("    > ERROR[{0}]: {1}".format(result.status, result.detail))
            aergo.disconnect()
            return
        else:
            print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))

        time.sleep(3)

        print("------ Check deployment of SC -----------")
        print("  > TX: {}".format(simple_tx.tx_hash))
        tx_result = aergo.get_tx_result(simple_tx.tx_hash)
        print("      result: ", tx_result)

        aergo.get_account()
        print("    > account state of Sender")
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Create Tx -----------")
        tx = herapy.Transaction(from_address=bytes(sender_account.address),
                                nonce=sender_account.nonce + 1,
                                amount=10)
        tx.to_address = herapy.utils.decode_address(receiver_address)
        print("  > unsigned TX Hash: {}".format(tx.tx_hash))
        print("  > unsigned TX : {}".format(herapy.utils.convert_tx_to_formatted_json(tx)))

        print("------ Sign Tx -----------")
        tx.sign = sender_account.sign_msg_hash(tx.calculate_hash(including_sign=False))
        print("  > TX Signature: {}".format(tx.sign_str))
        print("  > TX Hash: {}".format(tx.tx_hash))
        print("  > TX : {}".format(herapy.utils.convert_tx_to_formatted_json(tx)))

        print("------ Send Tx -----------")
        txs, results = aergo.send_tx(tx)
        for i, tx in enumerate(txs):
            print("  > TX[{}]".format(i))
            print("{}".format(herapy.utils.convert_tx_to_formatted_json(tx)))
            if result.status != herapy.CommitStatus.TX_OK:
                eprint("    > ERROR[{0}]: {1}".format(result.status, result.detail))
                aergo.disconnect()
                return
            else:
                print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))

        # wait to generate a block
        time.sleep(3)

        aergo.get_account()
        print("    > account state of Sender")
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

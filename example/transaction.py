import grpc
import time

import herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address_str))
        state = aergo.get_account_state(sender_account)
        print("    > account state : {}".format(state))
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Set Receiver Account -----------")
        receiver_address_str = "AmNHbk46L5ZaFH942mxDrunhUb34S8xRd7ygNnqaW5nqJDt5ugKD"
        receiver_address = herapy.Account.decode_address(receiver_address_str)
        print("  > Receiver Address: {}".format(receiver_address_str))

        print("------ Simple Send Tx -----------")
        simple_tx, result = aergo.send_payload(to_address=receiver_address,
                                               amount=10, payload=None, retry_nonce=3)
        print("  > simple TX[{}]".format(simple_tx.calculate_hash()))
        print("{}".format(herapy.convert_tx_to_json(simple_tx)))
        if int(result['error_status']) != herapy.CommitStatus.TX_OK:
            print("    > ERROR[{0}]: {1}".format(result['error_status'], result['detail']))
        else:
            print("    > result : {}".format(result))

        print("------ Create Tx -----------")
        tx = herapy.Transaction(from_address=sender_account.address,
                                nonce=sender_account.nonce + 1,
                                amount=10)
        tx.to_address = receiver_address
        print("  > unsigned TX Hash: {}".format(tx.calculate_hash(including_sign=False)))
        print("  > unsigned TX Hash: {}".format(tx.tx_hash_str))
        print("  > unsigned TX : {}".format(herapy.convert_tx_to_json(tx)))

        print("------ Sign Tx -----------")
        tx.sign = sender_account.sign_msg_hash(tx.calculate_hash(including_sign=False))
        print("  > TX Signature: {}".format(tx.sign_str))
        print("  > TX Hash: {}".format(tx.calculate_hash()))
        print("  > TX Hash: {}".format(tx.tx_hash_str))
        print("  > TX : {}".format(herapy.convert_tx_to_json(tx)))

        print("------ Send Tx -----------")
        txs, results = aergo.send_tx(tx)
        for i in range(len(txs)):
            print("  > TX[{}]".format(i))
            print("{}".format(herapy.convert_tx_to_json(txs[i])))
            if int(results[i]['error_status']) != herapy.CommitStatus.TX_OK:
                print("    > ERROR: {}".format(results[i]['detail']))
            else:
                print("    > result : {}".format(results[i]))

        # wait to generate a block
        time.sleep(60)

        state = aergo.get_account_state(sender_account)
        print("    > account state : {}".format(state))
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

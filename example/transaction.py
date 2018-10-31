import grpc

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

        print("------ Set Receiver Account -----------")
        receiver_address_str = "AmLeRAq94xu44YESvK5D5LgXwUBCPZ4LX8tGyF1Eo3urQ59uzDdy"
        receiver_address = herapy.Account.decode_address(receiver_address_str)
        print("  > Receiver Address: {}".format(receiver_address_str))

        print("------ Simple Send Tx -----------")
        simple_tx, result = aergo.send_payload(to_address=receiver_address,
                                               amount=10, payload=None)
        print("  > simple TX : {}".format(herapy.convert_tx_to_json(simple_tx)))
        print("  > simple TX result : {}".format(result))

        print("------ Simple Send Tx -----------")
        simple_tx, result = aergo.send_payload(to_address=receiver_address,
                                               amount=10, payload='')
        print("  > simple TX : {}".format(herapy.convert_tx_to_json(simple_tx)))
        print("  > simple TX result : {}".format(result))

        print("------ Create Tx -----------")
        tx = herapy.Transaction(from_address=sender_account.address,
                                nonce=sender_account.nonce + 1,
                                amount=10)
        tx.to_address = receiver_address
        print("  > unsigned TX Hash: {}".format(tx.calculate_hash()))
        print("  > unsigned TX Hash: {}".format(tx.tx_hash_str))
        print("  > unsigned TX : {}".format(herapy.convert_tx_to_json(tx)))

        print("------ Sign Tx -----------")
        signature = sender_account.sign_message(tx.calculate_hash())
        tx.sign = signature
        print("  > TX Signature: {}".format(tx.sign_str))
        print("  > TX Hash: {}".format(tx.calculate_hash()))
        print("  > TX Hash: {}".format(tx.tx_hash_str))
        print("  > TX : {}".format(herapy.convert_tx_to_json(tx)))

        print("------ Send Tx -----------")
        #tx_id = aergo.send_tx(tx)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

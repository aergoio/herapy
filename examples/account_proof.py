import grpc

import aergo.herapy as herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        address = "AmPwBMCcYbqyetVmAupjtzR8GgnTAVduZAVE9SnJPzjhWEmhjSef"

        print("------ Fund a second account to pass test in testmode -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(password="test password", private_key=sender_private_key)
        aergo.get_account()
        simple_tx, result = aergo.send_payload(to_address=address,
                                               amount=10, payload=None, retry_nonce=3)
        if result.status != herapy.CommitStatus.TX_OK:
            print("    > ERROR[{0}]: {1}".format(result.status, result.detail))
        else:
            print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))



        print("------ Get Account State -----------")
        account = aergo.get_account(address=address, proof=True)
        print("  > account state in 'aergo'")
        print('    - Nonce:        %s' % aergo.account.nonce)
        print('    - Balance:      %s' % aergo.account.balance)
        print('    - Code Hash:    %s' % aergo.account.code_hash)
        print('    - Storage Root: %s' % aergo.account.storage_root)

        print("\n account.state :\n ", account.state)
        print("\n account.state_proof :\n", account.state_proof)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Create Account failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

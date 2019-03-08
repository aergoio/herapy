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

        address = "AmPwBMCcYbqyetVmAupjtzR8GgnTAVduZAVE9SnJPzjhWEmhjSef"

        print("------ Fund a second account to pass test in testmode -------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        aergo.new_account(private_key=sender_private_key)
        simple_tx, result = aergo.send_payload(to_address=address,
                                               amount=10, payload=None,
                                               retry_nonce=3)
        if result.status != herapy.CommitStatus.TX_OK:
            eprint("    > ERROR[{0}]: {1}".format(result.status, result.detail))
        else:
            print("    > result[{0}] : {1}".format(result.tx_id,
                                                   result.status.name))

        print("------ Get Account State -----------")
        best_block_hash, best_block_height = aergo.get_blockchain_status()
        block = aergo.get_block(best_block_hash)
        root = block.blocks_root_hash
        account = aergo.get_account(address=address, proof=True, root=root)
        account2 = aergo.get_account(address=address, proof=True,
                                     compressed=False, root=root)

        print("account = {}".format(account))
        print("account.balance = {}".format(account.balance.aergo))
        print("account2 = {}".format(account2))
        print("account2.balance = {}".format(account2.balance.aergo))

        print("------ Verify inclusion proof -----------")
        print("valid inclusion proof compressed: ",
              account.verify_proof(root))
        print("valid inclusion proof: ", account2.verify_proof(root))

        print("------ Verify Non inclusion proof -----------")
        address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
        account = aergo.get_account(address=address, proof=True, root=root)
        account2 = aergo.get_account(address=address, proof=True,
                                     compressed=False, root=root)
        print(account)
        print(account2)
        print("valid exclusion proof compressed: ",
              account.verify_proof(root))
        print("valid exclusion proof: ", account2.verify_proof(root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

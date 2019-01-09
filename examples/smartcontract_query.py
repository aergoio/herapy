import sys
import traceback
import time

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def run():
    print("------ Payload -----------")
    """
        -- Define global variables.
        state.var {
            a = state.value(),
        }

        function constructor(name)
            a:set(name)
        end

        function set_name(name)
            a:set(name)
        end

        function get_name()
            return a:get()
        end

        function test_array(array)
            a:set(array[1])
        end

        function say_hello()
            a:set("hello")
        end


        abi.register(set_name, get_name, test_array, say_hello)
    """
    payload_str = "Ar1NzSMULGWsUVZCAfZxris1bDV1BYSXASj3ogDyjiC3R6FPRCNfLZCV7zHS1sMFuYwmeTcH8nuKvgb5V8uaWyw8kznwmpFJVqHPbmbiZvyMCvCfwsJjnLSFv5mMhaWjVZpf83FCyEibZhphnmaYCaF7h7AAVr3jVETAPuRBHS39wMJLe8e4uatUpf7wnPo6fXiLREbti1BuXyyEtELysDXbkA7exJeSPQRd2Gnzc1nz8t4AQGBrWDbtfHKvarGDHGzfutQqAtYkmjbKTtxvEjLBqsytZcRBgqkT6727iXb2uk2tQfTSgV5P5TA911sdXeCr26FMqLVFqVXJuhK4MzUjiedBoeoWAMWqKp4eK4k5D6bhwyyVyWDkq4kbt2wjGnfw7P2ssTUUoQ8SoLc5cJPjgLMrr2s4sT1o9tUfrFVKWj5BtakzC5pHaUqvksZq4ZUrq95ZRQBmexXpXDJ6tJF4mor2qoR5miQWy68ERVFbLzjSgbNaS5LpfyBTDueGbXHN8FAeHjw1Uh49YEtc61zgMd1Lw1XWN8PvW93nKmBYXtbr1yKeFfTocShR7t1buFJ4pEV8t15K3hKUuVeSbaZPZgkvKg7WvV8zi8hjLiQGefRBggsSeZzFrVToGLubhTRAs4mBzQuZubw8To6BD1CfvCt3XsUJzabZnuWiBJQrVdeLVWUjbCEZnoGCdPPTLt3iUcXY3yXEtTFdLUJPs2EQXx88Ctbnnf1APRMgT6QvxBxwC58vr2yRR828MV9Eft1CpULDCT5LWR2vePZgS9UwZN81PftWQ4T2f2WoRYJbnLiQJGbWyimkjMzYQgfU6mr3XLVMDvhu1ETZfLDK685U9M"
    payload = herapy.utils.decode_address(payload_str)

    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('testnet.aergo.io:7845')

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address))
        print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

        aergo.get_account()
        print("    > account state of Sender")
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Deploy SC -----------")
        tx, result = aergo.deploy_sc(amount=0, payload=payload, args=1234)
        print("  > TX: {}".format(tx.tx_hash))
        print("{}".format(herapy.utils.convert_tx_to_json(tx)))
        if result.status != herapy.CommitStatus.TX_OK:
            eprint("    > ERROR[{0}]: {1}".format(result.status, result.detail))
            aergo.disconnect()
            return
        else:
            print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))
            print(herapy.utils.convert_bytes_to_int_str(bytes(tx.tx_hash)))

        time.sleep(3)

        print("------ Check deployment of SC -----------")
        print("  > TX: {}".format(tx.tx_hash))
        result = aergo.get_tx_result(tx.tx_hash)
        if result.status != herapy.SmartcontractStatus.CREATED:
            eprint("  > ERROR[{0}]:{1}: {2}".format(
                result.contract_address, result.status, result.detail))
            aergo.disconnect()
            return

        sc_address = result.contract_address
        print("  > SC Address: {}".format(sc_address))

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "get_name")
        print(result)

        print("------ Query SC State Var with Proof -----------")
        best_block_hash, best_block_height = aergo.get_blockchain_status()
        block = aergo.get_block(best_block_hash)
        root = block.blocks_root_hash
        result = aergo.query_sc_state(sc_address, "a", root=root)
        print(result)
        print(result.var_proof.var_proof.value)
        print("valid inclusion proof compressed:",
              result.verify_inclusion(root))
        result = aergo.query_sc_state(sc_address, "a", root=root,
                                      compressed=False)
        print(result)
        print("valid inclusion proof:", result.verify_inclusion(root))

        result = aergo.query_sc_state(sc_address, "not included var",
                                      root=root)
        print("valid exclusion proof compressed:",
              result.verify_exclusion(root))
        result = aergo.query_sc_state(sc_address, "not included var",
                                      root=root, compressed=False)
        print("valid exclusion proof :", result.verify_exclusion(root))


        address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
        result = aergo.query_sc_state(address, "a", root=root)
        print("valid exclusion proof unknown address compressed:",
              result.verify_exclusion(root))
        result = aergo.query_sc_state(address, "a", root=root,
                                      compressed=False)
        print("valid exclusion proof unknown address:",
              result.verify_exclusion(root))


        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

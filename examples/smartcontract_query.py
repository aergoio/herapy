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
            b = state.value(),
            c = state.value(),
        }

        function constructor(name)
            a:set("a_" .. name)
            b:set("b_" .. name)
            c:set("c_" .. name)
        end

        function set_name(key, name)
            if key == "a" then
                a:set(name)
            elseif key == "b" then
                b:set(name)
            else
                c:set(name)
            end
        end

        function get_name(key)
            if key == "a" then
                a:get()
            elseif key == "b" then
                b:get()
            else
                c:get()
            end
        end

        function test_array(key, array)
            if key == "a" then
                a:set(array[1])
            elseif key == "b" then
                b:set(array[1])
            else
                c:set(array[1])
            end
        end

        function say_hello()
            a:set("hello A")
            b:set("hello B")
            c:set("hello C")
        end


        abi.register(set_name, get_name, test_array, say_hello)
    """
    payload_str = "SwLu5Jt217gMrbi2ApmQzTRYxBBJdP6Sp65VZfsSLUASo3GYwLbm4Zu2rvJtZoEJuWQAYVNpBY2YCFqn9YCmSyKftLYacAxSt44GB1F5VYqXdftpCQPMgzmYLyw5YkeP6Kmp58JxPdtFwDt721PhSi9hxb6unv7ZzCqqTh2TSUg9bo66ZLyULZdYRiPdk1uFarRVV8wtkPGeZQYmpMBRKzkew8o8PTCDuavHwHJZNKoyXcg1dT7TZfk5p7xQE4kgKZov8rYhoKSJN9Y3cbh5rwhzwwUnPtWEo4jMcfksz3fJQKdvYzp89ZZUVJ8hfQhoLgDnqnqcRh5bq9nQZjiDuLpWB9eo33uWpPzaV64zgrime6QsSia1LH89boqD7PwzJEfYL31XpxNHpbeLCQNE79LYAvkaMPhgm8MvoefvrWksEM2wVSLABgfxMZm6yAhB7YfvHuyeumdFTEQjZnvTGzDxv9RfepTWVbBJ9TSgEyzvSx1V7qG3AHkbCpzr4amKvxpT7igRy696nRHTT4ZKuDiZEWMMPybUQAE4mNbg3RQaFjW3bMDYp59mfyjwp3trzwhD1iMRG4TAWF68sobsbi1fzAbaJQYb7vreg8FuLw26K8581E5FqjGvKoKhS7MfT84aqcu1f7KnWRQhK9WsRVn8wipaWsQE14TzYeZUm92cnS1QdrRtCgWaNt3JDaDCbwBgJL8D4Ku2XaozEz6kCsTk7VHKQbm88BpfzXNKReJxnRZ8AbX1C7k5eHpjkBKfMYgeD7kSheJSPTSGToVWoF3oGA2RHE2xdQ8GW16XJJZD1xQjaPkj4u6CiBYWRGHxUj1PqwK6svNkLJSRczVqdU6JGAXqfAkZwfkX9Rcs6H55GagK46XmybH5CZXHaKDTrgQZZ6zeRzzTZHfkJdVL3C1hGsUFZQaZmyecUvonUFi6VE3jeFFTSK7a7aL1EFawjbN8bEFAkUDzUoEe2dp6gvCJyfmKSZD4Jzii7tKi6NUSkt759uba41F1v22JaWEmRwN9jSDdJ3HntDXUp9mBnhG3VK9y8a1dCFjC35bSM913i1ipDNXDn7L4xs1aTwwkiiARs8qd7SVF1PKv1ThhQYoxCzV9CTu6VsCWPRuevDhdujdMjmyhFRF1HMNgWm7ZVyEcdsAcfggkk1TXQJqxdoGnsJLXuRUVa6Hb9gkEEa19Z8NdZ3ztSa437p5xS3WkqQRSRTqMuTMBJ5x9EstjDMeM9uUaW9PfEWWQ19agj9WLL4ymRuiVLc5x4tUk1qVAQSUNPAvPH6kUWgcr3iLCsUNKpo5C1Qzm82vBPqGTT7LtrTaq4FoDLsmNN2ULx98EUSRpzSNcVqZgM74uJwGftuPMx6aqxx9kagBtkBGJyAb9aMbDuKyvhZ3RZQAi54GGBJbnHyjc86wATpgYFFvSvuuFQvawF9f1Hc1qX18SyaRQUPLEM5mRLQCN6nDMqGpmgu6h6CrvNnL3cr7jz8aToYCAodNuFaqk2n9rxe7Lwt7cNeiM7UFMMgpAFYPpA5sUxGjJw8t72HqhUVZS8ovfTKGhkRWStjfbKdGP"
    payload = herapy.utils.decode_address(payload_str)

    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

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
        if result.status != herapy.TxResultStatus.CREATED:
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

        sc_states = aergo.query_sc_state(sc_address,
                                         [{'key':'a', 'index':None}, ['b', ], 'c'],
                                         root=root)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid inclusion proof:",
                  sc_state.verify_inclusion(root))
            print()

        sc_states = aergo.query_sc_state(sc_address, ['a', 'b', 'c'], root=root, compressed=False)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid inclusion proof:",
                  sc_state.verify_inclusion(root))
            print()

        sc_states = aergo.query_sc_state(sc_address, ['not', 'included', 'var'], root=root)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid exclusion proof:",
                  sc_state.verify_exclusion(root))
            print()

        sc_states = aergo.query_sc_state(sc_address, ['not', 'included', 'var'], root=root, compressed=False)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid exclusion proof:",
                  sc_state.verify_exclusion(root))
            print()

        address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
        sc_states = aergo.query_sc_state(address, ["a"], root=root)
        print("valid inclusion proof unknown address compressed:",
              sc_states[0].verify_inclusion(root))
        print("valid exclusion proof unknown address compressed:",
              sc_states[0].verify_exclusion(root))
        sc_states = aergo.query_sc_state(address, ["a"], root=root, compressed=False)
        print("valid inclusion proof unknown address:",
              sc_states[0].verify_inclusion(root))
        print("valid exclusion proof unknown address:",
              sc_states[0].verify_exclusion(root))

        # combination of variables exist and not-exist
        sc_states = aergo.query_sc_state(sc_address, ['a', '_sv_b', 'c', 'abc', 'b'], root=root)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid inclusion proof:",
                  sc_state.verify_inclusion(root))
        sc_states = aergo.query_sc_state(sc_address, ['a', '_sv_b', 'c', 'abc', 'b'], root=root, compressed=False)
        for i, sc_state in enumerate(sc_states):
            print("[{0}] Compressed? {1}".format(i, sc_state.compressed))
            print("  var_proof.key          = {}".format(sc_state.var_proof.key))
            print("  var_proof.value        = {}".format(sc_state.var_proof.value))
            print("  var_proof.inclusion    = {}".format(sc_state.var_proof.inclusion))
            print("  var_proof.proof_key    = {}".format(sc_state.var_proof.proof_key))
            print("  var_proof.proof_value  = {}".format(sc_state.var_proof.proof_value))
            print("  var_proof.bitmap       = {}".format(sc_state.var_proof.bitmap))
            print("  var_proof.height       = {}".format(sc_state.var_proof.height))
            print("  valid inclusion proof:",
                  sc_state.verify_inclusion(root))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception:
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

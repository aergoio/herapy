import sys
import traceback
import time

import aergo.herapy as herapy
from aergo.herapy.obj.sc_state import SCStateVar


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    print("------ Payload -----------")
    """
        -- Define global variables.
        state.var {
            a = state.value(),
            b = state.array(3),
            c = state.map(),
        }

        function constructor(name)
            a:set("a_" .. name)
            b[1] = "b_" .. name
            c["init"] = "c_" .. name
        end

        function set_name(key, name)
            if key == "a" then
                a:set(name)
            elseif key == "b" then
                b[2] = name
            else
                c['name'] = name
            end
        end

        function get_name(key)
            if key == "a" then
                return a:get()
            elseif key == "b" then
                return b[2]
            else
                return c['name']
            end
        end

        function say_hello()
            a:set("hello A")
            b[3] = "hello B"
            c["hello"] = "hello C"
        end

        abi.register(set_name, get_name, say_hello)
    """
    payload_str = "2Jzi8odjCSuGxVM4TVcUt8S5zKHcoZdqrzQ7vfPvSMhTez6hDzd4ZcpQr18roCbaDBtdsWRBHQV1eGkzegNTPrshcHvXf1sSmP62YCNSvYzBDbhv5qkDjhK3qAE2x1MdUKUtJjMZ1Y9ZXQDFSwjzAkYomv7SnLr4fDfYEGdhULtc3LWsiafswkJXu1c4wiVg4hfQDgXepBR5o7qoSYdN7tKtRLP9X3gkqJX1Y8FauETxzewMWZWhDAJYbEL5PY8C1gtDzf9jG7446xHWEj2AMyu2KN7dnGQzUoFshYFE9CtbzRRGUJqUdx9EPbqC3VvqrqsJDYsn31UeUGfAfgVMxb2uig8cAqSVb8AKM7TVqZfXWcQdcvEgYnDb9ujSpyiazQpxYAtchenDeyU9Mud4yNNNQHW1zsJcZpgPiHdDRbZDwmiiJ4h6bA3fBwCujNqEkTHL5H8RgaFZ65WbthtpKV5FiLfu22YCaL8BP7YLQd2zKDQZdAVgtWndqUyKEJ9tAvcKd2ZoM7KLsusGvFkoCerqhRktVAvyjrsUh9ttSY6bcCX3F8gz7nfzuFGQ9UggNBtBCSMxLfWARugVrifBL8D2kA2BqA9Q67Vk4fTss5iHsVPunaEQaJCBvBWrda2fn6tKoDy5vM27zaN81tmMisR76r9M3SfjGZbWcaFDRqN8SFmnP4t9L9EcVgWaquKkGzchqQY5kvTZSphJkvBa9HoEjc8JQaMxuXj2mzwpzmcRM7EXMJSVRTBKbhekH1zNus7QWeq2G8iLP4jwKjcLT9cRj9MRCj5Tkfs4tMKQrVo72LN3JBTc5rNBGgHRE9uHb39bfNqpzvURPAxP7AREyJhVuzjaNmEbYo5Zw1b73TnKFPYTRa4SpDFajopoRa8KpBU6m6XhRpRNWW6eYWahF9gnYX2qYjeEzz27a7xuSEwW2Bx8LqoQzSVpkJ1qoVYLzWqCDPDzEPS295vnbrABnL6Q3vhaAG4nGqtnkftkWVSakESKRz5YcedQe2Y8t51J2hPS8k3t7VGQoYUxvdMSwyYcKBiRXMjCPxZ7QUKTd42Snwhmcy5s6PMbzdxGJT1EvUL2hJ9wMfVqkFkJoSJ2UXmjJE31J7KBCmpUiicAopDfrYAzgKnRHiTyPRmi3oFJe1KGBg9iuNJKQsEHvykySnuooyZhGoXChSMV4HMVBBr9LHajQE23TEJoQSSGihUHb38wtgpHm4r1APi95npgPcwJnRde7CyHJw8MAd7sUiGq"
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

        print("------ Query SC State Var with Proof -----------")
        best_block_hash, best_block_height = aergo.get_blockchain_status()
        block = aergo.get_block(best_block_hash)
        root = block.blocks_root_hash
        sc_state = aergo.query_sc_state(sc_address, ["_sv_a"], root=root)
        sc_root = sc_state.account.state_proof.state.storageRoot
        print("Variable Proof: {}".format(sc_state.var_proofs.verify_var_proof(root=sc_root,
                                                                               var_proof=sc_state.var_proofs[0])))
        print("Variables Proof: {}".format(sc_state.var_proofs.verify_proof(root=sc_root)))
        print("Total Proof: {}".format(sc_state.verify_proof(root)))

        sc_state = aergo.query_sc_state(sc_address, ["_sv_a", "_sv_b-1", "_sv_c-init"], root=root)
        print("Proof: {}".format(sc_state.verify_proof(root)))
        for i, vp in enumerate(sc_state.var_proofs):
            print("[{0}] Variable Proof: {1}".format(i, sc_state.var_proofs.verify_var_proof(root=sc_root,
                                                                                             var_proof=vp)))
            print("  var_proof.key          = {}".format(vp.key))
            print("  var_proof.value        = {}".format(vp.value))
            print("  var_proof.inclusion    = {}".format(vp.inclusion))
            print("  var_proof.proof_key    = {}".format(vp.proofKey))
            print("  var_proof.proof_value  = {}".format(vp.proofVal))
            print("  var_proof.bitmap       = {}".format(vp.bitmap))
            print("  var_proof.height       = {}".format(vp.height))

        sc_var_a = SCStateVar(var_name="a")
        sc_var_b = SCStateVar(var_name="b", array_index=1)
        sc_var_c = SCStateVar(var_name="c", map_key='init')
        sc_state = aergo.query_sc_state(sc_address, [sc_var_a, sc_var_b, sc_var_c], root=root, compressed=False)
        print("Proof: {}".format(sc_state.verify_proof(root)))

        sc_state = aergo.query_sc_state(sc_address, ['not', 'included', 'var'], root=root)
        for i, vp in enumerate(sc_state.var_proofs):
            print("var[{}]".format(i))
            print("  key: {}".format(vp.key))
            print("  inclusion? {}".format(vp.inclusion))
        print("not inclusion? Proof = {}".format(sc_state.verify_proof(root)))

        sc_state = aergo.query_sc_state(sc_address, ['not', 'included', 'var'], root=root, compressed=False)
        for i, vp in enumerate(sc_state.var_proofs):
            print("var[{}]".format(i))
            print("  key: {}".format(vp.key))
            print("  inclusion? {}".format(vp.inclusion))
        print("not inclusion? Proof = {}".format(sc_state.verify_proof(root)))

        address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
        sc_state = aergo.query_sc_state(address, ["_sv_a"], root=root)
        sc_root = sc_state.account.state_proof.state.storageRoot
        print("Number of Variable Proofs = {}".format(len(sc_state.var_proofs)))
        print("Variables Proof: {}".format(sc_state.var_proofs.verify_proof(root=sc_root)))
        print("Total Proof: {}".format(sc_state.verify_proof(root)))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

import hashlib
import sys
import traceback
import time

import aergo.herapy as herapy
from aergo.herapy.obj.sc_state import SCStateVar


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    print("------ Contract Code -----------")
    contract_code = """
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
            c[string.char(0x01)] = name
            c[fromhex('61')] = name
        end

        function fromhex(str)
            return (str:gsub('..', function (cc)
                return string.char(tonumber(cc, 16))
            end))
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

        print("------ Deploy Smart Contract -----------")
        tx, result = aergo.deploy_contract(contract_code=contract_code, args=1234)
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
        print("Variable Proof: {}".format(sc_state.var_proofs.verify_var_proof(
            sc_root, sc_state.var_proofs[0], hashlib.sha256(bytes("_sv_a", 'latin-1')).digest())))
        print("Variables Proof: {}".format(sc_state.var_proofs.verify_proof(root=sc_root)))
        print("Total Proof: {}".format(sc_state.verify_proof(root)))

        storage_keys = ["_sv_a", "_sv_b-1", "_sv_c-init", "_sv_c-\x01", "_sv_c-a"]
        sc_state = aergo.query_sc_state(sc_address, storage_keys, root=root)
        print("Proof: {}".format(sc_state.verify_proof(root)))
        for i, vp in enumerate(sc_state.var_proofs):
            print("[{0}] Variable Proof: {1}".format(i, sc_state.var_proofs.verify_var_proof(
                sc_root, vp, hashlib.sha256(bytes(storage_keys[i], 'latin-1')).digest())))
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

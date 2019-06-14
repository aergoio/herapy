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
    payload_str = "MyFxtNVdegMvf25CroFLsQs1H8mNXEdTwT7QTHYakg8gx8EJdivi87GJpLu9RUmEB7kECTMhcEeNYNRF7uW1rozSCBJameJZejrs2u39E57zebBCmTvp4331tAeVTQzr5B4PCt6xVd9UtU4kCBiL4Jfi8YJpu9jE3cJ5qpW39yZCoaSNMRWEsoDLePn1tBxnvvKTzP37o7Zges9gLoThS6G7ioH6cFQhSxV9fPBoPfE1b6zMoSi97tyaDDc1XjDJ4YCLLBhaVeN55ZY5ayjajBCoKXGTUp8yiQNkGx3Jy5YwYPZxnvtiYxzpoKZtYz3nA6QRgkC16ecFtGBM8GYzFhYoDQpse24yjQfqwH5SkQh6EHGzUaCzX7AahivvjkyAtdpS5kfbJqquYUoYHoqXXLcLTj5CZ9Wzck6mdq25o8sQmM8DBnQ3DX6QQyyY9agCcRHYkK5Zr52vDmigsXS1qXJfDvBmrUTsvXFMfPE3EZUV5PaYTNubS7AGjReWQpou5FCpkshoAdfoiLLHTa1yCZJdCbjv8gpPWJCeivFbUo6Y2Xp41HreLExnZHHpEeZvEgat8ArA24ardELWWiVeE9ZkW3VE7gReDUJNWStZBrASNje7N8GsHhdvdKSKGJ8LAFkF4MrDSH4hPpjZkK6PJBu2jCuX9VoMUcR3p6RJ6NZFf7JudiWEkkZx7kULbeN31rpAhm3bXgFnU8eiamQk4ddY2Qur6kfzjCTmdu9SUwi71b778LsmxsosqbpoFnbvUhBuZKrjuNA1uJdhSoErDe6RkpkP5bm6asszpNK7zBu5iUyn1VepnbCyG2zWdeK7UQufcLGQh8yFamY2FqKpBkxaXkSFyfSjE41VT2mgGFhkMdz4E5ddmPjSg4RGYw33V1tCq3sRtFRe34zR3HrRsr54yFLLMbS1tyzt6tMREAghhTgXaKt9akigkeunczpntdRcBFzNgGqBx2BHyBXaRPzUWWdouvCBjaUzeZuxKVhodU1uts6tHQJWjk4yvgSmDB1mooTaYTuHAWgCLrjUEMyTNZWkdsgKkxfZtV5Q8rbqJ8FGQvSCucXDjFyCy5XPf5GNxhvdj7qYuewMxMM428qF6cR8MBqCo9LX85iRPCKdSVksAedk1GWehVAzwqGMGgMAE21P1EzCdTf3khhkXNT5xxYHtYVGtFUoWPKqi5Xr1jc6h3yYVPjXuUvYPPCDYQU6mboSSAfr211XFsJS42WRF2xHVFRn3jT76kgqfNxbCfXeWrcRVJfLcwE9FACfXGbp7GdUUZbcYKjCCjJ68W6qznwbZuph9oCiPsM1Y4A4UaesSwoijVUHxwSgZc1uJWjBBzuV1APQGTW7Z6DhfoZKfKhtDabTQhrafoUB9ZCbCqqDdTSGBufYRJ6qsSqTfr15YEyKgzdy5juRrXADF17P3f4XCeerD5N8neUjsUfVa8BWFuQfDWeHskzGWtLQnVs2qfhqM8tUefuMBEp2vG3CgRe247WKDLPPHpPeeern7PWiJgf5JzRt9h3brCcQy5qp39KKznEdrVrS6iNMEBK5qjtPHSqFbdSkkYEbqRp6gdisSPGFS2jraXFi2x"
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

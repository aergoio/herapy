import hashlib

import aergo.herapy as herapy
from aergo.herapy.obj.sc_state import SCStateVar


def test_sc_query(aergo) -> None:
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

    payload_str = "MyFxtNVdegMvf25CroFLsQs1H8mNXEdTwT7QTHYakg8gx8EJdivi87GJp" \
        "Lu9RUmEB7kECTMhcEeNYNRF7uW1rozSCBJameJZejrs2u39E57zebBCmTvp4331tAeV" \
        "TQzr5B4PCt6xVd9UtU4kCBiL4Jfi8YJpu9jE3cJ5qpW39yZCoaSNMRWEsoDLePn1tBx" \
        "nvvKTzP37o7Zges9gLoThS6G7ioH6cFQhSxV9fPBoPfE1b6zMoSi97tyaDDc1XjDJ4Y" \
        "CLLBhaVeN55ZY5ayjajBCoKXGTUp8yiQNkGx3Jy5YwYPZxnvtiYxzpoKZtYz3nA6QRg" \
        "kC16ecFtGBM8GYzFhYoDQpse24yjQfqwH5SkQh6EHGzUaCzX7AahivvjkyAtdpS5kfb" \
        "JqquYUoYHoqXXLcLTj5CZ9Wzck6mdq25o8sQmM8DBnQ3DX6QQyyY9agCcRHYkK5Zr52" \
        "vDmigsXS1qXJfDvBmrUTsvXFMfPE3EZUV5PaYTNubS7AGjReWQpou5FCpkshoAdfoiL" \
        "LHTa1yCZJdCbjv8gpPWJCeivFbUo6Y2Xp41HreLExnZHHpEeZvEgat8ArA24ardELWW" \
        "iVeE9ZkW3VE7gReDUJNWStZBrASNje7N8GsHhdvdKSKGJ8LAFkF4MrDSH4hPpjZkK6P" \
        "JBu2jCuX9VoMUcR3p6RJ6NZFf7JudiWEkkZx7kULbeN31rpAhm3bXgFnU8eiamQk4dd" \
        "Y2Qur6kfzjCTmdu9SUwi71b778LsmxsosqbpoFnbvUhBuZKrjuNA1uJdhSoErDe6Rkp" \
        "kP5bm6asszpNK7zBu5iUyn1VepnbCyG2zWdeK7UQufcLGQh8yFamY2FqKpBkxaXkSFy" \
        "fSjE41VT2mgGFhkMdz4E5ddmPjSg4RGYw33V1tCq3sRtFRe34zR3HrRsr54yFLLMbS1" \
        "tyzt6tMREAghhTgXaKt9akigkeunczpntdRcBFzNgGqBx2BHyBXaRPzUWWdouvCBjaU" \
        "zeZuxKVhodU1uts6tHQJWjk4yvgSmDB1mooTaYTuHAWgCLrjUEMyTNZWkdsgKkxfZtV" \
        "5Q8rbqJ8FGQvSCucXDjFyCy5XPf5GNxhvdj7qYuewMxMM428qF6cR8MBqCo9LX85iRP" \
        "CKdSVksAedk1GWehVAzwqGMGgMAE21P1EzCdTf3khhkXNT5xxYHtYVGtFUoWPKqi5Xr" \
        "1jc6h3yYVPjXuUvYPPCDYQU6mboSSAfr211XFsJS42WRF2xHVFRn3jT76kgqfNxbCfX" \
        "eWrcRVJfLcwE9FACfXGbp7GdUUZbcYKjCCjJ68W6qznwbZuph9oCiPsM1Y4A4UaesSw" \
        "oijVUHxwSgZc1uJWjBBzuV1APQGTW7Z6DhfoZKfKhtDabTQhrafoUB9ZCbCqqDdTSGB" \
        "ufYRJ6qsSqTfr15YEyKgzdy5juRrXADF17P3f4XCeerD5N8neUjsUfVa8BWFuQfDWeH" \
        "skzGWtLQnVs2qfhqM8tUefuMBEp2vG3CgRe247WKDLPPHpPeeern7PWiJgf5JzRt9h3" \
        "brCcQy5qp39KKznEdrVrS6iNMEBK5qjtPHSqFbdSkkYEbqRp6gdisSPGFS2jraXFi2x"

    payload = herapy.utils.decode_address(payload_str)

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
    assert result.status == herapy.CommitStatus.TX_OK, \
        "    > ERROR[{0}]: {1}".format(result.status, result.detail)
    print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))
    print(herapy.utils.convert_bytes_to_int_str(bytes(tx.tx_hash)))

    aergo.wait_tx_result(tx.tx_hash)

    print("------ Check deployment of SC -----------")
    print("  > TX: {}".format(tx.tx_hash))
    result = aergo.get_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.CREATED, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    sc_address = result.contract_address
    print("  > SC Address: {}".format(sc_address))

    print("------ Query SC State Var with Proof -----------")
    best_block_hash, best_block_height = aergo.get_blockchain_status()
    block = aergo.get_block(best_block_hash)
    root = block.blocks_root_hash
    sc_state = aergo.query_sc_state(sc_address, ["_sv_a"], root=root)
    sc_root = sc_state.account.state_proof.state.storageRoot
    assert sc_state.var_proofs.verify_var_proof(
        sc_root, sc_state.var_proofs[0],
        hashlib.sha256(bytes("_sv_a", 'latin-1')).digest()
    ) is True, "Invalid variable proof"
    assert sc_state.var_proofs.verify_proof(root=sc_root) is True, \
        "Invalid variable proof"
    assert sc_state.verify_proof(root) is True, "Invalid total proof"

    storage_keys = ["_sv_a", "_sv_b-1", "_sv_c-init", "_sv_c-\x01", "_sv_c-a"]
    sc_state = aergo.query_sc_state(sc_address, storage_keys, root=root)
    assert sc_state.verify_proof(root) is True, "Invalid total proof"
    for i, vp in enumerate(sc_state.var_proofs):
        assert sc_state.var_proofs.verify_var_proof(
            sc_root, vp,
            hashlib.sha256(bytes(storage_keys[i], 'latin-1')).digest()
        ) is True, "Invalid variable proof {}".format(i)
        print("  var_proof.key          = {}".format(vp.key))
        print("  var_proof.value        = {}".format(vp.value))
        print("  var_proof.inclusion    = {}".format(vp.inclusion))
        assert vp.inclusion is True
        print("  var_proof.proof_key    = {}".format(vp.proofKey))
        print("  var_proof.proof_value  = {}".format(vp.proofVal))
        print("  var_proof.bitmap       = {}".format(vp.bitmap))
        print("  var_proof.height       = {}".format(vp.height))

    sc_var_a = SCStateVar(var_name="a")
    sc_var_b = SCStateVar(var_name="b", array_index=1)
    sc_var_c = SCStateVar(var_name="c", map_key='init')
    sc_state = aergo.query_sc_state(
        sc_address, [sc_var_a, sc_var_b, sc_var_c], root=root,
        compressed=False
    )
    assert sc_state.verify_proof(root) is True, "Invalid total proof"

    sc_state = aergo.query_sc_state(
        sc_address, ['not', 'included', 'var'], root=root)
    for i, vp in enumerate(sc_state.var_proofs):
        print("var[{}]".format(i))
        print("  key: {}".format(vp.key))
        assert vp.inclusion is False
    assert sc_state.verify_proof(root) is True, "Invalid non inclusion proof"

    sc_state = aergo.query_sc_state(
        sc_address, ['not', 'included', 'var'], root=root, compressed=False)
    for i, vp in enumerate(sc_state.var_proofs):
        print("var[{}]".format(i))
        print("  key: {}".format(vp.key))
        assert vp.inclusion is False
    assert sc_state.verify_proof(root) is True, "Invalid non inclusion proof"

    address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
    sc_state = aergo.query_sc_state(address, ["_sv_a"], root=root)
    sc_root = sc_state.account.state_proof.state.storageRoot
    assert len(sc_state.var_proofs) == 0, \
        "There shouldn't be var proofs if contract doesnt exist"
    assert sc_state.var_proofs.verify_proof(root=sc_root) is False, \
        "Var proof verification should be false if there is no proof"
    assert sc_state.verify_proof(root) is False, \
        "Total proof should be False if contract doesnt exist"

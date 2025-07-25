import aergo.herapy as herapy


def test_sc(aergo) -> None:
    print("------ Contract Code -----------")
    contract_code = """
-- Define global variables
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

    print("------ Set Receiver Account -----------")
    receiver_address = "AmNHbk46L5ZaFH942mxDrunhUb34S8xRd7ygNnqaW5nqJDt5ugKD"
    print("  > Receiver Address: {}".format(receiver_address))

    print("------ Deploy Smart Contract -----------")
    tx, result = aergo.deploy_contract(contract_code=contract_code, args=1234)
    print("  > TX: {}".format(tx.tx_hash))
    print("{}".format(herapy.utils.convert_tx_to_json(tx)))
    assert result.status == herapy.CommitStatus.TX_OK, \
        "    > ERROR[{0}]: {1}".format(result.status, result.detail)
    print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))
    print(herapy.utils.convert_bytes_to_int_str(bytes(tx.tx_hash)))

    aergo.wait_tx_result(tx.tx_hash)
    aergo.get_account()

    print("------ Check deployment of SC -----------")
    print("  > TX: {}".format(tx.tx_hash))
    result = aergo.get_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.CREATED, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    sc_address = result.contract_address
    print("  > SC Address: {}".format(sc_address))

    print("------ Fail SC -----------")
    tx, result = aergo.call_sc(sc_address, "set_none")
    aergo.wait_tx_result(tx.tx_hash)
    result = aergo.get_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.ERROR, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    print("------ Query SC -----------")
    result = aergo.query_sc(sc_address, "get_name")
    assert result == b'1234'

    print("------ Call SC -----------")
    tx, result = aergo.call_sc(sc_address, "test_array", args=[["a", "b"]])

    print("-------Wait for tx result--------")
    result = aergo.wait_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.SUCCESS, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    print("------ Check result of Call SC -----------")
    print("  > TX: {}".format(tx.tx_hash))
    result = aergo.get_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.SUCCESS, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    print("------ Query SC -----------")
    result = aergo.query_sc(sc_address, "get_name")
    assert result == b'"a"'

    print("------- Get smart contract abi --------")
    abi = aergo.get_abi(sc_address)
    # Check that 'say_hello' function is in the ABI functions list
    function_names = [func['name'] for func in abi.functions]
    assert 'say_hello' in function_names

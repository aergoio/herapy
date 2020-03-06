import aergo.herapy as herapy


def test_aergo_enterprise_contract() -> None:
    SC_ADDRESS = herapy.GovernanceTxAddress.ENTERPRISE
    """
    const SetConf = "setConf"
    const AppendConf = "appendConf"
    const RemoveConf = "removeConf"
    const AppendAdmin = "appendAdmin"
    const RemoveAdmin = "removeAdmin"
    const EnableConf = "enableConf"
    const DisableConf = "disableConf"
    const ChangeCluster = "changeCluster"
    """
    aergo = herapy.Aergo()

    print("------ Connect AERGO -----------")
    aergo.connect('localhost:7848')

    print("------ Set Admin Account -----------")
    sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
    sender_account = aergo.new_account(private_key=sender_private_key)
    print("  > Admin Address: {}".format(sender_account.address))
    assert sender_account.address
    print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

    aergo.get_account()
    print("    > account state of Sender")
    print("      - balance        = {}".format(sender_account.balance))
    print("      - nonce          = {}".format(sender_account.nonce))
    print("      - code hash      = {}".format(sender_account.code_hash))
    print("      - storage root   = {}".format(sender_account.storage_root))

    print("------ Call SC: appendAdmin -----------")
    tx, result = aergo.call_sc(
        SC_ADDRESS, "appendAdmin", args=[str(sender_account.address)])
    print(result)

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

    config = aergo.get_enterprise_config('ADMINS')
    print(config.values)
    assert config.values == [str(sender_account.address)]

    print("------ Call SC: removeAdmin -----------")
    tx, result = aergo.call_sc(
        SC_ADDRESS, "removeAdmin", args=[str(sender_account.address)])

    print("-------Wait for tx result--------")
    result = aergo.wait_tx_result(tx.tx_hash)
    print(result)
    assert result.status == herapy.TxResultStatus.SUCCESS, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)

    print("------ Check result of Call SC -----------")
    print("  > TX: {}".format(tx.tx_hash))
    result = aergo.get_tx_result(tx.tx_hash)
    assert result.status == herapy.TxResultStatus.SUCCESS, \
        "  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail)
    config = aergo.get_enterprise_config('ADMINS')
    print(config.values)
    assert config.values == []

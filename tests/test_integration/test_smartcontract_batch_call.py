import aergo.herapy as herapy
import datetime


def test_sc_batch(aergo) -> None:
    print("------ Payload -----------")
    """
-- 'payload' is compiled by aergoluac from
function setItem(key, value)
    system.print('setItem: key='..key..', value='..value)
    system.setItem(key, value)
end

function getItem(key)
    system.print('getItem: key='..key)
    return system.getItem(key)
end

abi.register(setItem, getItem)
    """

    payload_str = "246oyQ629vXweGRbeS8r29poBjGsiqJL23BBaYh8TaSgvGhMAXHrk9vUX" \
        "etphe6m9xCPrRDpQH3fHap4SZUpNWartsHTnJxQXp2zs5mMwK5cwiCgSCePwefA1U4f" \
        "wyt94Q249MxQ2evTKc7vcUVjjn6AnKCqMJTGCgVtnLrpeVMiVEcYBszJtprA3YQmgA8" \
        "vsnfcw5ocw4149wDhV8drF4zviYJSfhGP5TRj7NhLLBstiktq2DzPW8yCrVu2fEnyzf" \
        "Jc1yY9ENuu2K7LyxC7arqGTafZEzsQrrfNo63PXfsSq6oSW7Ev89Y3cFfRjpQfr8mHZ" \
        "PmfCRykUF7aepvkH64r6S7Sg3uUpgrZCnDKuDRuBCizBHUxJDUCua3tJNA2dKFtx9dp" \
        "STfPFkdvPoBFsTjegu6DwHgDop5zZMPV5S4Q5oi5vB1UsvSoX81cMAfp38kJe45ko9r" \
        "LZKk83zpSfgzMLnjDZWccmjtNdnHFhUp9KZG3JRZnr7QRmAHwvTYLd83AS9uCVJhwg5" \
        "oGhVNgMeTnN2f1xZ9Gd9C5NfJTvwYHPVysD7HRwyXVTwYgQhjxwTrxkGcz54gJzF2eT" \
        "DqWnEQKZN61322SZG"

    payload = herapy.utils.decode_address(payload_str)
    print(''.join('{:d} '.format(x) for x in payload))

    byte_code_len = int.from_bytes(payload[:4], byteorder='little')
    print("payload: byte code length = ", byte_code_len)

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
        "  > ERROR[{0}]:{1}: {2}".format(result.contract_address,
                                         result.status, result.detail)

    sc_address = result.contract_address
    print("  > SC Address: {}".format(sc_address))

    print("------ Batch Call SC -----------")
    time_start = datetime.datetime.now()
    nonce = aergo.account.nonce + 1
    total_tx_cnt = 1000
    sc_txs = []
    for i in range(total_tx_cnt):
        sc_txs.append(aergo.new_call_sc_tx(sc_address, "setItem",
                                           args=["key{}".format(i),
                                                 "value{}".format(i)],
                                           nonce=nonce + i))
    aergo.batch_call_sc(sc_txs)

    print("------ Check result of Batch Call SC -----------")
    for i, tx in enumerate(sc_txs):
        print("  > TX[{0}] Result: {1}".format(i, str(tx.tx_hash)))
        result = aergo.wait_tx_result(tx.tx_hash)
        assert result.status == herapy.TxResultStatus.SUCCESS, \
            "  > ERROR[{0}]:{1}: {2}".format(
                result.contract_address, result.status, result.detail)
        assert sc_address == result.contract_address

    time_diff = datetime.datetime.now() - time_start
    time_diff_min = int(time_diff.seconds / 60)
    time_diff_sec = int(time_diff.seconds % 60)
    time_diff_mil = int(time_diff.microseconds / 1000)
    time_diff_mic = int(time_diff.microseconds % 1000)
    print("Execution time: {} = "
          "{} min, {} secs, "
          "{} milli, {} micro".format(time_diff.total_seconds(),
                                      time_diff_min,
                                      time_diff_sec,
                                      time_diff_mil,
                                      time_diff_mic))

    print("------ Query SC -----------")
    for i in range(total_tx_cnt):
        key = "key{}".format(i)
        value = "\"value{}\"".format(i).encode()
        assert value == aergo.query_sc(sc_address, "getItem", args=[key])

import aergo.herapy as herapy


def test_tx_batch(aergo) -> None:
    print("------ Set Sender Account -----------")
    sender_private_key = \
        "eHoEcHnaxpGpgzknXjuwon8VFVrLkKHC4FckGuGkQ8depiDDfyUAWC3L"
    sender_account = aergo.new_account(private_key=sender_private_key)
    print("  > Sender Address: {}".format(sender_account.address))
    aergo.get_account()
    print("    > account state of Sender")
    print("      - balance        = {}".format(sender_account.balance))
    print("      - nonce          = {}".format(sender_account.nonce))
    print("      - code hash      = {}".format(sender_account.code_hash))
    print("      - storage root   = {}".format(sender_account.storage_root))

    print("------ Set Receiver Account -----------")
    receiver_address = "AmMPQqRJ4pd8bS9xdkw5pjExtLjaUXaYGB5kagzHu4A9ckKgnBV2"
    print("  > Receiver Address: {}".format(receiver_address))
    receiver_account = aergo.get_account(address=receiver_address)
    print("    > account state of Sender")
    print("      - balance        = {}".format(receiver_account.balance))
    print("      - nonce          = {}".format(receiver_account.nonce))
    print("      - code hash      = {}".format(receiver_account.code_hash))
    print("      - storage root   = {}".format(receiver_account.storage_root))

    print("------ Send batch Txs -----------")
    nonce = sender_account.nonce
    txs = [
        aergo.generate_tx(
            to_address=receiver_address, nonce=nonce + 1, amount='9 aer'),
        aergo.generate_tx(
            to_address=receiver_address, nonce=nonce + 2, amount='90 aer'),
        aergo.generate_tx(
            to_address=receiver_address, nonce=nonce + 3, amount='900 aer'),
        aergo.generate_tx(
            to_address=receiver_address, nonce=nonce + 4, amount='9000 aer'),
        aergo.generate_tx(
            to_address=receiver_address, nonce=nonce + 5, amount='90000 aer'),
    ]

    txs, results = aergo.batch_tx(signed_txs=txs)
    for i, tx in enumerate(txs):
        print("[{}]".format(i))
        print("  > tx: ", str(tx))
        result = results[i]
        print("  > result: ", result)
        assert result.status == herapy.CommitStatus.TX_OK, \
            "    > ERROR[{0}]: {1}".format(
                herapy.CommitStatus(result.status).name, result.detail)
        print("    > result[{0}] : {1}"
              .format(result.tx_id, result.status.name))

    aergo.wait_tx_result(txs[-1].tx_hash)

    print("------ Check TX status -----------")
    for i, tx in enumerate(txs):
        print("[{}]".format(i))
        print("  > tx: ", str(tx))
        tx_result = aergo.get_tx_result(tx.tx_hash)
        print("      result: ", tx_result)
        assert tx_result.status == herapy.TxResultStatus.SUCCESS, \
            "  > ERROR[{0}]:{1}: {2}".format(
                tx_result.contract_address, tx_result.status, tx_result.detail)

    print("------ Get Sender Account Info -----------")
    aergo.get_account()
    print("    > account state of Sender")
    print("      - balance        = {}".format(sender_account.balance))
    print("      - nonce          = {}".format(sender_account.nonce))
    print("      - code hash      = {}".format(sender_account.code_hash))
    print("      - storage root   = {}".format(sender_account.storage_root))

import aergo.herapy as herapy


def test_account_json(aergo) -> None:
    print("------ Set Sender Account -----------")
    sender_json = '{' \
        '"address": "AmNW9YMMm48jTxX5Yee6tRYLpuptWdg3cqbD2CVoee1YcUGBHfad",'\
        '"enc_key": "47QHSuhBTZ4b7nbw2zJz5EARyQ4XS8gDxhFDeu5mYeKNqfHhwRutU' \
        'mja3WRxV1suB12eWBeDZ"}'
    sender_account = herapy.Account.from_json(sender_json, password='5678')
    print("  > Sender Account before connecting: {}".format(sender_account))
    print("     > address:     {}".format(sender_account.address))
    print("     > private key: {}".format(sender_account.private_key))

    print("------ Set Sender Account -----------")
    aergo.account = sender_account
    aergo.get_account()
    print("  > Sender Account after connecting: {}".format(aergo.account))

    print("------ Set Receiver Account -----------")
    receiver_json = \
        '{"address": "AmMPQqRJ4pd8bS9xdkw5pjExtLjaUXaYGB5kagzHu4A9ckKgnBV2"}'
    receiver_account = herapy.Account.from_json(receiver_json)
    receiver_account = aergo.get_account(account=receiver_account)
    print("  > Receiver Account: {}".format(receiver_account))

    print("------ Simple Transfer -----------")

    print("------ Check Account Info Before -----------")
    aergo.get_account()
    print("  > Sender Account: {}".format(aergo.account))
    receiver_account = aergo.get_account(receiver_account)
    print("  > Receiver Account: {}".format(receiver_account))
    receiver_balance_before = int(receiver_account.balance)

    amount = 10000000000
    simple_tx, result = aergo.transfer(to_address=receiver_account.address,
                                       amount=amount)
    print("  > simple TX[{}]".format(simple_tx.calculate_hash()))
    print("{}".format(str(simple_tx)))
    print("  > result: ", result)
    assert result.status == herapy.CommitStatus.TX_OK, \
        "Tx didn't commit: {}, {}".format(result.status, result.detail)
    print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))

    aergo.wait_tx_result(simple_tx.tx_hash)

    print("------ Check Account Info After -----------")
    aergo.get_account()
    print("  > Sender Account: {}".format(aergo.account))
    receiver_account = aergo.get_account(receiver_account)
    print("  > Receiver Account: {}".format(receiver_account))

    assert int(receiver_account.balance) == \
        int(receiver_balance_before) + amount

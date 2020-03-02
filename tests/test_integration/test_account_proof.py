import aergo.herapy as herapy


def test_account_proof(aergo) -> None:
    address = "AmPwBMCcYbqyetVmAupjtzR8GgnTAVduZAVE9SnJPzjhWEmhjSef"

    print("------ Fund a second account to pass test in testmode -------")
    sender_private_key = \
        "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
    aergo.new_account(private_key=sender_private_key)
    simple_tx, result = aergo.send_payload(to_address=address,
                                           amount=10, payload=None,
                                           retry_nonce=3)
    assert result.status == herapy.CommitStatus.TX_OK, \
        "    > ERROR[{0}]: {1}".format(result.status, result.detail)
    print("    > result[{0}] : {1}".format(result.tx_id, result.status.name))
    aergo.wait_tx_result(simple_tx.tx_hash)

    print("------ Get Account State -----------")
    best_block_hash, best_block_height = aergo.get_blockchain_status()
    block = aergo.get_block(best_block_hash)
    root = block.blocks_root_hash
    account = aergo.get_account(address=address, proof=True, root=root)
    account2 = aergo.get_account(address=address, proof=True,
                                 compressed=False, root=root)

    print("account = {}".format(account))
    print("account.balance = {}".format(account.balance.aergo))
    print("account2 = {}".format(account2))
    print("account2.balance = {}".format(account2.balance.aergo))
    assert int(account.balance) == int(account2.balance)

    print("------ Verify inclusion proof -----------")
    assert account.state_proof.inclusion is True
    assert account2.state_proof.inclusion is True
    assert account.verify_proof(root) is True, \
        "Invalid inclusion proof compressed"
    assert account2.verify_proof(root) is True, \
        "Invalid inclusion proof compressed"

    print("------ Verify Non inclusion proof -----------")
    address = "AmMejL8z3wW2doksBzzMiWM2xTb6WtZniLkLyxwqWKiLJKK8Yvqd"
    account = aergo.get_account(address=address, proof=True, root=root)
    account2 = aergo.get_account(address=address, proof=True,
                                 compressed=False, root=root)
    print(account)
    print(account2)
    assert account.state_proof.inclusion is False
    assert account2.state_proof.inclusion is False
    assert account.verify_proof(root) is True, \
        "Invalid exclusion proof compressed"
    assert account2.verify_proof(root) is True, \
        "Invalid exclusion proof compressed"

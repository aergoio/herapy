import aergo.herapy as herapy


def test_sc_event(aergo) -> None:
    print("------ Payload -----------")
    """

function constructor(name)
        contract.event("movie", "robocop", 1, "I'll be back")
end

function movie_event(name)
        contract.event("movie", "arnold", 2, "It's mine")
        contract.event("movie", "terminator", 3, "No, it's mine")
end

function ani_event(name)
        contract.event("a-time!!")
        contract.event("a-time!!", "pinn", "Adventure time!!", false,
                       bignum.number("999999999999999"),
                       {"princess bubble gum", 1}
        )
        contract.event("a-time!!", "Jake", "Adventure time!!", false,
                       {"whatever", 1, {true, false},
                        bignum.number("999999999999999")}
        )

        contract.event("movie", "yoda", 3, "i'm not the ani character.")
end

abi.register(movie_event, ani_event)
    """
    payload_str = "D1ZsfUyj4q8GA6AtbW81TzSTSvqaeUvcsePsaZufptRK5qSb83fyXRWdE" \
        "gGhLWs17JfRNrM4iLjGe54fkyvsyjHVgFCHqTzJWK4Yz8uQwRqzF5x1g1twZ3jPP1Xt" \
        "J95y43RD48qXGoeeoDsmmNErQJCux6d4eLZwE344bz5hM1DdWEd22yE6ogC37RLRtRZ" \
        "5FFKm3HkxaM67G7VqWfsX5t2Tmd23Myn62hkAdNWjSBaWizqyi6ENB3VD2YJGG82bVe" \
        "q9a4zMQdK58Wxnfcfqo14Vo9Y9jsY8A5QYNRi6uotRfiYt3LFrPjPBWgyQRn4qFQypS" \
        "W5vfgFZvv9VBdFPGgoMN5zeBp7VNWXvE5o8CGAf3fuFu2gCGLS4DfCtQe7VNnsCUi7U" \
        "1AdmdupqoxMHM6kCfEtk77YyiaaSTm4xUSt7R2hwzs2Xnfh8CLxMaH2cg3rsWF4fefs" \
        "5KvnjN3F1q43og6BueK66o8NssyY41kAtincbYhDC8oHaBkMTdXD6mkhb3QECwn8dh8" \
        "k9a3KTys1tdUzf99nqpK5YrAcZFDjbrmmmtcBYwZg6zdRAkQnJptvr25HzeHMfbfERH" \
        "8P1XzYmjqYynFvUNv4utuWZ7avS2xvJoZph3nSa8Xuhbdw6TFLVCDZVfZB6j8kQbJnb" \
        "1DoEEtvhPHLMP4StcgiE9grGQuduZ5iHYtS8Nk696Fq6Y9gzp19bWD3VKarq1XuueM6" \
        "FNrzCQNY22nov4mxbM8vcxp4axdjmZNWLcdttFycazorxCNbn1YBQFzGPGzstJPN72R" \
        "B9dxV17cb1TuREKTF7mVLLeahgHsY4eVnA1m5Z8U7tFKswRDTGeXv6vCt7MstVBztdd" \
        "4sRfHTXKdFCgfoQk2zwzGS8FEVgxAP3Y4Tip4nuQd8hVyTiaApFmNnkD9byxUNCc44T" \
        "r9LAnRycc239HGpZjWBwsJvmb4jsY2fuEELXfSgQf4yZhnbcPC4DYPQLDRXc8E6DdLz" \
        "ixMk7cAfUZqododk9SWzjB9FSKtzVYWiKuyg2uZoRaxDmrtZpe6pXL8F4pzt2P2HEG6" \
        "jyFn5MT9PBWhkj11vqAjWpdRgNAbTKEb5zk9ZeER9YUAT8etk2VFpAGqmGnv9CTEQr2" \
        "rfDQeNgNYzoy44mNZonhi4n4zo9h2HmrSsatWa8oxbJJYihGs7zD65TiqRfnKg43Xx5" \
        "qD"

    payload = herapy.utils.decode_address(payload_str)
    print(''.join('{:d} '.format(x) for x in payload))

    byte_code_len = int.from_bytes(payload[:4], byteorder='little')
    print("payload: byte code length = ", byte_code_len)

    print("------ Set Sender Account -----------")
    sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
    sender_account = aergo.new_account(private_key=sender_private_key)
    print("  > Sender Address: {}".format(sender_account.address))
    print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

    print("------ Deploy SC -----------")
    tx, result = aergo.deploy_sc(amount=0, payload=payload, args=1234,
                                 retry_nonce=5)
    print("  > TX: {}".format(tx.tx_hash))
    print("{}".format(str(tx)))
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

    print("------ Get events -----------")
    events = aergo.get_events(sc_address, "movie", with_desc=True,
                              arg_filter={0: 'arnold'})
    print("how many 'arnold' in movie? {}".format(len(events)))
    assert len(events) == 0

    events = aergo.get_events(sc_address, "movie", with_desc=True,
                              arg_filter={0: 'robocop'})
    print("how many 'robocop' in movie? {}".format(len(events)))
    assert len(events) == 1

    event_block_no = 0
    for i, e in enumerate(events):
        event_block_no = e.block_height
        print("[{}] Event: {}".format(i, str(e)))

    events = aergo.get_events(
        sc_address, "movie", end_block_no=event_block_no - 1)
    print("in history: how many movie? {}".format(len(events)))
    assert len(events) == 0

    events = aergo.get_events(
        sc_address, "movie", start_block_no=event_block_no + 1)
    print("after: how many movie? {}".format(len(events)))
    assert len(events) == 0

    print("------ Call SC -----------")
    tx, result = aergo.call_sc(sc_address, "movie_event")
    print("movie_event tx hash: {}".format(str(tx.tx_hash)))
    aergo.wait_tx_result(tx.tx_hash)

    print("------ Get events -----------")
    events = aergo.get_events(sc_address, "movie")
    print("how many 'movie'? {}".format(len(events)))
    assert len(events) == 3
    for i, e in enumerate(events):
        print("[{}] Event: {}".format(i, str(e)))
    events = aergo.get_events(sc_address, "a-time!!")
    print("how many 'a-time!!'? {}".format(len(events)))
    assert len(events) == 0

    print("------ Call SC -----------")
    tx, result = aergo.call_sc(sc_address, "ani_event")
    print("ani_event tx hash: {}".format(str(tx.tx_hash)))
    aergo.wait_tx_result(tx.tx_hash)

    print("------ Get events -----------")
    events = aergo.get_events(sc_address, "movie")
    print("how many 'movie'? {}".format(len(events)))
    assert len(events) == 4
    events = aergo.get_events(sc_address, "a-time!!")
    print("how many 'a-time!!'? {}".format(len(events)))
    assert len(events) == 3
    for i, e in enumerate(events):
        print("[{}] Event: {}".format(i, str(e)))

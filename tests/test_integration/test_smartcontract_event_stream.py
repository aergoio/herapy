import time

from threading import Thread

import aergo.herapy as herapy


def read_movie_event_stream(movie_event_stream) -> None:
    while True:
        try:
            print("RECEIVE: 'movie' Event: {}"
                  .format(str(next(movie_event_stream))))
            print(movie_event_stream.is_active())
            print(movie_event_stream.cancelled())
            print(movie_event_stream.done())
            print(movie_event_stream.running())
        except Exception as e:
            print(e)
            print(movie_event_stream.is_active())
            print(movie_event_stream.cancelled())
            print(movie_event_stream.done())
            print(movie_event_stream.running())
            break

    print("END 'movie' event stream")
    movie_event_stream.stop()


def test_sc_event_stream(aergo) -> None:
    print("------ Contract Code -----------")
    contract_code = """

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

    print("------ Set Sender Account -----------")
    sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
    sender_account = aergo.new_account(private_key=sender_private_key)
    print("  > Sender Address: {}".format(sender_account.address))
    print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

    print("------ Deploy Smart Contract -----------")
    tx, result = aergo.deploy_contract(amount=0, contract_code=contract_code, args=1234)
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

    print("------ Get reading events threads -----------")
    movie_event_stream = aergo.receive_event_stream(
        sc_address, "movie", start_block_no=0)
    movie_thread = Thread(target=read_movie_event_stream,
                          args=[movie_event_stream])
    movie_thread.start()

    print("------ Call SC -----------")
    tx, result = aergo.call_sc(sc_address, "movie_event")
    print("movie_event tx hash: {}".format(str(tx.tx_hash)))
    aergo.wait_tx_result(tx.tx_hash)

    print("------ Cancel 'movie' event stream -----------")
    movie_event_stream.cancel()

    while True:
        if movie_event_stream.stopped:
            break
        time.sleep(1)

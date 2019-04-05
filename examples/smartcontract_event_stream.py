import sys
import traceback
import time

from threading import Thread

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def read_movie_event_stream(movie_event_stream):
    while True:
        try:
            print("RECEIVE: 'movie' Event: {}".format(str(next(movie_event_stream))))
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


def run():
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
        contract.event("a-time!!", "pinn", "Adventure time!!", false, bignum.number("999999999999999"), {"princess bubble gum", 1})
        contract.event("a-time!!", "Jake", "Adventure time!!", false, {"whatever", 1, {true, false}, bignum.number("999999999999999")})

        contract.event("movie", "yoda", 3, "i'm not the ani character.")
end

abi.register(movie_event, ani_event)
    """
    payload_str = "D1ZsfUyj4q8GA6AtbW81TzSTSvqaeUvcsePsaZufptRK5qSb83fyXRWdEgGhLWs17JfRNrM4iLjGe54fkyvsyjHVgFCHqTzJWK4Yz8uQwRqzF5x1g1twZ3jPP1XtJ95y43RD48qXGoeeoDsmmNErQJCux6d4eLZwE344bz5hM1DdWEd22yE6ogC37RLRtRZ5FFKm3HkxaM67G7VqWfsX5t2Tmd23Myn62hkAdNWjSBaWizqyi6ENB3VD2YJGG82bVeq9a4zMQdK58Wxnfcfqo14Vo9Y9jsY8A5QYNRi6uotRfiYt3LFrPjPBWgyQRn4qFQypSW5vfgFZvv9VBdFPGgoMN5zeBp7VNWXvE5o8CGAf3fuFu2gCGLS4DfCtQe7VNnsCUi7U1AdmdupqoxMHM6kCfEtk77YyiaaSTm4xUSt7R2hwzs2Xnfh8CLxMaH2cg3rsWF4fefs5KvnjN3F1q43og6BueK66o8NssyY41kAtincbYhDC8oHaBkMTdXD6mkhb3QECwn8dh8k9a3KTys1tdUzf99nqpK5YrAcZFDjbrmmmtcBYwZg6zdRAkQnJptvr25HzeHMfbfERH8P1XzYmjqYynFvUNv4utuWZ7avS2xvJoZph3nSa8Xuhbdw6TFLVCDZVfZB6j8kQbJnb1DoEEtvhPHLMP4StcgiE9grGQuduZ5iHYtS8Nk696Fq6Y9gzp19bWD3VKarq1XuueM6FNrzCQNY22nov4mxbM8vcxp4axdjmZNWLcdttFycazorxCNbn1YBQFzGPGzstJPN72RB9dxV17cb1TuREKTF7mVLLeahgHsY4eVnA1m5Z8U7tFKswRDTGeXv6vCt7MstVBztdd4sRfHTXKdFCgfoQk2zwzGS8FEVgxAP3Y4Tip4nuQd8hVyTiaApFmNnkD9byxUNCc44Tr9LAnRycc239HGpZjWBwsJvmb4jsY2fuEELXfSgQf4yZhnbcPC4DYPQLDRXc8E6DdLzixMk7cAfUZqododk9SWzjB9FSKtzVYWiKuyg2uZoRaxDmrtZpe6pXL8F4pzt2P2HEG6jyFn5MT9PBWhkj11vqAjWpdRgNAbTKEb5zk9ZeER9YUAT8etk2VFpAGqmGnv9CTEQr2rfDQeNgNYzoy44mNZonhi4n4zo9h2HmrSsatWa8oxbJJYihGs7zD65TiqRfnKg43Xx5qD"
    payload = herapy.utils.decode_address(payload_str)
    print(''.join('{:d} '.format(x) for x in payload))

    byte_code_len = int.from_bytes(payload[:4], byteorder='little')
    print("payload: byte code length = ", byte_code_len)

    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address))
        print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

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

        print("------ Get reading events threads -----------")
        movie_event_stream = aergo.receive_event_stream(sc_address, "movie",
                                                        start_block_no=0)
        movie_thread = Thread(target=read_movie_event_stream,
                              args=[movie_event_stream])
        movie_thread.start()

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "movie_event")
        print("movie_event tx hash: {}".format(str(tx.tx_hash)))
        time.sleep(3)

        print("------ Cancel 'movie' event stream -----------")
        movie_event_stream.cancel()

        while True:
            if movie_event_stream.stopped:
                break
            time.sleep(3)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

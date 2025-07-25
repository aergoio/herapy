import sys
import traceback
import time

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
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
        contract.event("a-time!!", "pinn", "Adventure time!!", false, bignum.number("999999999999999"), {"princess bubble gum", 1})
        contract.event("a-time!!", "Jake", "Adventure time!!", false, {"whatever", 1, {true, false}, bignum.number("999999999999999")})

        contract.event("movie", "yoda", 3, "i'm not the ani character.")
end

abi.register(movie_event, ani_event)
    """

    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address))
        print(herapy.utils.convert_bytes_to_int_str(bytes(sender_account.address)))

        print("------ Deploy Smart Contract -----------")
        tx, result = aergo.deploy_contract(contract_code=contract_code, args=1234,
                                     retry_nonce=5)
        print("  > TX: {}".format(tx.tx_hash))
        print("{}".format(str(tx)))
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

        print("------ Get events -----------")
        events = aergo.get_events(sc_address, "movie", with_desc=True,
                                  arg_filter={0:'arnold'})
        print("how many 'arnold' in movie? {}".format(len(events)))
        events = aergo.get_events(sc_address, "movie", with_desc=True,
                                  arg_filter={0:'robocop'})
        print("how many 'robocop' in movie? {}".format(len(events)))
        event_block_no = 0
        for i, e in enumerate(events):
            event_block_no = e.block_height
            print("[{}] Event: {}".format(i, str(e)))
        events = aergo.get_events(sc_address, "movie",
                                  end_block_no=event_block_no-1)
        print("in history: how many movie? {}".format(len(events)))
        events = aergo.get_events(sc_address, "movie",
                                  start_block_no=event_block_no+1)
        print("after: how many movie? {}".format(len(events)))

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "movie_event")
        print("movie_event tx hash: {}".format(str(tx.tx_hash)))
        time.sleep(3)

        print("------ Get events -----------")
        events = aergo.get_events(sc_address, "movie")
        print("how many 'movie'? {}".format(len(events)))
        for i, e in enumerate(events):
            print("[{}] Event: {}".format(i, str(e)))
        events = aergo.get_events(sc_address, "a-time!!")
        print("how many 'a-time!!'? {}".format(len(events)))

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "ani_event")
        print("ani_event tx hash: {}".format(str(tx.tx_hash)))
        time.sleep(3)

        print("------ Get events -----------")
        events = aergo.get_events(sc_address, "movie")
        print("how many 'movie'? {}".format(len(events)))
        events = aergo.get_events(sc_address, "a-time!!")
        print("how many 'a-time!!'? {}".format(len(events)))
        for i, e in enumerate(events):
            print("[{}] Event: {}".format(i, str(e)))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

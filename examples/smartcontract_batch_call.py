import sys
import traceback
import time

import aergo.herapy as herapy


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
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
    payload_str = "246oyQ629vXweGRbeS8r29poBjGsiqJL23BBaYh8TaSgvGhMAXHrk9vUXetphe6m9xCPrRDpQH3fHap4SZUpNWartsHTnJxQXp2zs5mMwK5cwiCgSCePwefA1U4fwyt94Q249MxQ2evTKc7vcUVjjn6AnKCqMJTGCgVtnLrpeVMiVEcYBszJtprA3YQmgA8vsnfcw5ocw4149wDhV8drF4zviYJSfhGP5TRj7NhLLBstiktq2DzPW8yCrVu2fEnyzfJc1yY9ENuu2K7LyxC7arqGTafZEzsQrrfNo63PXfsSq6oSW7Ev89Y3cFfRjpQfr8mHZPmfCRykUF7aepvkH64r6S7Sg3uUpgrZCnDKuDRuBCizBHUxJDUCua3tJNA2dKFtx9dpSTfPFkdvPoBFsTjegu6DwHgDop5zZMPV5S4Q5oi5vB1UsvSoX81cMAfp38kJe45ko9rLZKk83zpSfgzMLnjDZWccmjtNdnHFhUp9KZG3JRZnr7QRmAHwvTYLd83AS9uCVJhwg5oGhVNgMeTnN2f1xZ9Gd9C5NfJTvwYHPVysD7HRwyXVTwYgQhjxwTrxkGcz54gJzF2eTDqWnEQKZN61322SZG"
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

        aergo.get_account()
        print("    > account state of Sender")
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Set Receiver Account -----------")
        receiver_address = "AmNHbk46L5ZaFH942mxDrunhUb34S8xRd7ygNnqaW5nqJDt5ugKD"
        print("  > Receiver Address: {}".format(receiver_address))

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

        print("------ Batch Call SC -----------")
        nonce = aergo.account.nonce + 1
        sc_txs = [
            aergo.new_call_sc_tx(sc_address, "setItem", args=["key1", "value1"], nonce=nonce),
            aergo.new_call_sc_tx(sc_address, "setItem", args=["key2", "value2"], nonce=nonce+1),
            aergo.new_call_sc_tx(sc_address, "setItem", args=["key3", "value3"], nonce=nonce+2),
            aergo.new_call_sc_tx(sc_address, "setItem", args=["key4", "value4"], nonce=nonce+3),
            aergo.new_call_sc_tx(sc_address, "setItem", args=["key5", "value5"], nonce=nonce+4),
        ]
        aergo.batch_call_sc(sc_txs)

        time.sleep(3)

        print("------ Check result of Batch Call SC -----------")
        for i, tx in enumerate(sc_txs):
            print("  > TX[{0}] Result: {1}".format(i, str(tx.tx_hash)))
            result = aergo.get_tx_result(tx.tx_hash)
            if result.status != herapy.TxResultStatus.SUCCESS:
                eprint("  > ERROR[{0}]:{1}: {2}".format(
                    result.contract_address, result.status, result.detail))
                aergo.disconnect()
                return

            sc_address = result.contract_address
            print("  > SC Address: {}".format(sc_address))

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "getItem", args=["key1"])
        print(result)
        result = aergo.query_sc(sc_address, "getItem", args=["key2"])
        print(result)
        result = aergo.query_sc(sc_address, "getItem", args=["key3"])
        print(result)
        result = aergo.query_sc(sc_address, "getItem", args=["key4"])
        print(result)
        result = aergo.query_sc(sc_address, "getItem", args=["key5"])
        print(result)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

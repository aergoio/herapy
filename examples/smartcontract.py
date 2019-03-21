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
        -- Define global variables.
        state.var {
            a = state.value(),
        }

        function constructor(name)
            a:set(name)
        end

        function set_name(name)
            a:set(name)
        end

        function get_name()
            return a:get()
        end

        function test_array(array)
            a:set(array[1])
        end

        function say_hello()
            a:set("hello")
        end


        abi.register(set_name, get_name, test_array, say_hello)
    """
    payload_str = "2bTAKwCcCqs1n91vFF5YnBBcaTLNsxhqzGgM8vcVAG3HqQLp1uZZSwvmnj8CEEm9GTvogDf3r6ioqHjbfBisjRzwUJxr6msFuf4vVuzbWEXtbShu43ZpLbJdT1NECStCEDGFPRsn3pc7jQ1FumPGB9GwGY7Y7wNN1t4kLMQPNxJCmDFAwLA6BAyCGpzW2g5rtHuWodTMTposF4EBRxbvsXYWvrDYLTK7JGbDsq4neBzXVtmJjereb7i6fX8Fug1LJ9GgYskTKdqcBjugxEoipjsAALtnr7mcUPoPFygbQzXbHsW13UwjhBxKsEvWYZm1hC8QxCeiRbHdx8VY5ES2ugR8Dt4uhiboAbaLofpnGRcPofgFGXiwDfESQgNZBjHP1DeEzh7gGh6fzABcw3LSjQLC9RETFWyUnWY3dU4iqH3PsVNhBFgHCUepBBphvwPT6UoictgsWzsnFdf1peiDsfXFE9uSTKWDCMhqgaETSLZdn8QiGBwMvZ1pEkP6xmh9389mFXCZ4ERNGUGkk6xNfN7xdZhRCeXxZupgtNDREX5PrHPveXEMbzThAMV7Rqzy3MazDaCFxjkbUVgQjWsHYhwEBRMvYSd2p621nZzcb9GFbh9tpXhwoLYpLp89Qhi9oTy61AD2GVFgQmdWF9neD1GvauVkCNFzWmEUkdSU3F6yBRwBm2cs8oJEieFu1zETLsMyXydTN5WqHFuGs2PaV1XRwPVRLeYiwo2xmgJMssHaGtR8pmb8TrQpTJbJdgreCVn8GiGzYizvEcRz9m8aFdompJ2m2QR7TDLCCjZx2UqRJdcQZmyxEAtzjnCCgD7Gwj95ZHkFxzoEEHTLYbG6uaneRrQWnzabAaRe2392qJnEkiNug9gkdJfsRFapbVxupH9zkoAmFP5xoWeGrkknUw61E4tX"
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
        aergo.get_account()

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

        print("------ Fail SC -----------")
        tx, result = aergo.call_sc(sc_address, "set_none")
        time.sleep(3)
        result = aergo.get_tx_result(tx.tx_hash)
        print("  > ERROR[{0}]:{1}: {2}".format(
            result.contract_address, result.status, result.detail))

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "get_name")
        print(result)

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "test_array", args=[["a", "b"]])

        time.sleep(3)

        print("------ Check result of Call SC -----------")
        print("  > TX: {}".format(tx.tx_hash))
        result = aergo.get_tx_result(tx.tx_hash)
        if result.status != herapy.TxResultStatus.SUCCESS:
            eprint("  > ERROR[{0}]:{1}: {2}".format(
                result.contract_address, result.status, result.detail))
            aergo.disconnect()
            return

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "get_name")
        print(result)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

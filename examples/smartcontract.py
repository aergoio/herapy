import grpc
import time
import json

import aergo.herapy as herapy


def run():
    print("------ Payload -----------")
    """
        -- Define global variables.
        state.var {
            a = state.value(),
        }

        function constructor()
            a:set("A")
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
    payload_str = "4JoZBjZo4SojWi236wk77CBVZ1upiwJh6i2X1ctwLmSixp3kzhYPfU8YyVKaGjQXRULDNddwYdjVvyjp9bTV3fLDc7GAa4SgvnDYibFU5YE1owPMn3y7p8Vf7d2ynu3XAwkLuG9uXS29ivWYnfNYY6pHPtkH7wPjjgxpNnx4HSUVQDMGqYE9TBQqZhHS1Uiear7kGPy7SFHRkz5F5U6ooUHboAz6FwNNWGVTBUCimLP3tBsRpizF22E2PHNhpxVowfdh1sa9gxNT56mSR7d3snKMGttBPttteUNxXpPSTZ3HhLzrVPfYZHmfb9gvBrcP13b4mavfPNMPGZyBcKVSy5GAvyvigRg3ZzaL7moDtTzbyNMpTUEta3bpsjUyR3iput728DAL4qwgeSKyJDWSqJ2h9pomgz9PJpCfivsigh67ABWXMexUNAcpC8p1enoRTeDuLf6XLvgrtgJEfVPaPNKknRdiEaqVTMB3FUMmoadsUZ4PN6ZQrGuSoZvkUvF7gSUFSMAbpCtq82LivxhGdKkHBQSYZNe4WhV5432V4yMfVz3LvJSc7NtnWr89iJaBSySZjtE51Tbe8FFcESNLf6JbDrBsJeY4J3nY2SAVFWcsQrbRVZXrokNUgnetfCbVccc8w1Tzit8cGG61GtDgEieqVUYuXhacMqzi1W8p68vKCi5V8hJrNPoiB4uCiASJGvUw5qARDy4BK8rCUj6LGrHYdqAQEYm1KsoSxn55Kxt8MgSzWg13xGKGREojA4BvYrUrFt6iaxYCBWNnznZqUocL8YqW5edkfnRsjfc8Mj1cKTTt9snZKXQNtXHGso1dH7QS6w2K52XC1cJ4g7crtBxHuXzGU"
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
        sender_account = aergo.new_account(password="test", private_key=sender_private_key)
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
        tx, result = aergo.deploy_sc(amount=0, payload=payload)
        print("  > TX: {}".format(tx.tx_hash))
        print("{}".format(herapy.utils.convert_tx_to_json(tx)))
        if int(result['error_status']) != herapy.CommitStatus.TX_OK:
            print("    > ERROR[{0}]: {1}".format(result['error_status'], result['detail']))
        else:
            print("    > result : {}".format(json.dumps(result, indent=2)))
            print("      > result.hash : {}".format(result['hash']))
            print(''.join('{:d} '.format(x) for x in bytes(tx.tx_hash)))

        time.sleep(3)

        print("------ Check deployment of SC -----------")
        print("  > TX: {}".format(tx.tx_hash))
        sc_address, status, ret = aergo.get_tx_result(tx.tx_hash)
        if status != herapy.SmartcontractStatus.CREATED.value:
            print("  > ERROR[{0}]:{1}: {2}".format(sc_address, status, ret))
            aergo.disconnect()
            return
        print("  > SC Address: {}".format(sc_address))

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "test_array", args=[["a", "b"]])

        time.sleep(3)

        print("------ Check result of Call SC -----------")
        print("  > TX: {}".format(tx.tx_hash))
        sc_address, status, ret = aergo.get_tx_result(tx.tx_hash)
        if status != herapy.SmartcontractStatus.SUCCESS.value:
            print("  > ERROR[{0}]:{1}: {2}".format(sc_address, status, ret))
            aergo.disconnect()
            return
        print("  > SC Address: {}".format(sc_address))

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "get_name")
        print(result)

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

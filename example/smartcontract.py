import grpc
import base58
import time

import herapy


def run():
    try:
        aergo = herapy.Aergo()

        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Payload -----------")
        """
        'payload' is compiled by aergoluac from
function setItem(key, value)
  system.print('setItem: key='..key..', value='..value)
  system.setItem(key, value)
end

function getItem(key)
  system.print('getItem: key='..key)
  return system.getItem(key)
end

abi.register(setItem)
abi.register(getItem)
        """
        payload_str = "66F7XWcStRbqYNe9yeEHPUjCpJxuwQphf6G3NAz91wtMB9Zaa4hVq6s3pXpNtK5WRqi4aS9iNTyHmZN4sWDEvdjhEbvSCqUKAJBsuDSBhtkvrSD2dasKwZX7S5NBRoAuMrMEMRXVpDmQcoh37RBtSBCcB55QWNxgpztLzGJdhFRakqJ3FEQXQ3AzsrRGvULxgFUW4pt7Nb3ZQwgK7NBV2fHPxKA2PWYF6Qs2EifhYoLdyKxZzkdtjD6P2igRCn34EeUiRhYC7NLiAX4djnVEzcLdfjQyLWaauFyjXatCpAy1ajssL32aZs9AbRyMew5ozdDXRQgk1FNvsNq5H7eMQVG81ii6mNQJx6R5nen5ZPrCXZRLt353xniyFn1HNDAsn4TbTx5kkU7EgWAZj2tPcqokCLB7msZTnmFFaHcirdF6qFLFMzmoaaszqYeabiBekdcVRuVfBiozeL4b4i1fU4Q4ok4H96XN3H6KURtr1RzVy3rAoK13kbLQiXqdhshSV1GJaMS7By9HpQ2Nj6fuLok9kBk7MSENDq4cEmv63SV15PnKD5qfYgBYrZwJad1tZNJPWWixrUL5WCCf36J1DZ5M1zNQP6jLSUF9on4mCA9q3cdHbU"
        payload = herapy.Account.decode_address(payload_str)
        print(''.join('{:d} '.format(x) for x in payload))

        byte_code_len = int.from_bytes(payload[:4], byteorder='little')
        print("payload: byte code length = ", byte_code_len)

        result = aergo.query_sc("AmgRKV7n5WxiBRZwdwVQzCKYZoz9C4WfMmNZEDWoTALZTaASQJYi", "getItem", args=["key1"])
        print(result)
        return

        print("------ Set Sender Account -----------")
        sender_private_key = "6hbRWgddqcg2ZHE5NipM1xgwBDAKqLnCKhGvADWrWE18xAbX8sW"
        sender_account = aergo.new_account(private_key=sender_private_key)
        print("  > Sender Address: {}".format(sender_account.address_str))
        print(''.join('{:d} '.format(x) for x in sender_account.address))
        state = aergo.get_account_state(sender_account)
        print("    > account state : {}".format(state))
        print("      - balance        = {}".format(sender_account.balance))
        print("      - nonce          = {}".format(sender_account.nonce))
        print("      - code hash      = {}".format(sender_account.code_hash))
        print("      - storage root   = {}".format(sender_account.storage_root))

        print("------ Set Receiver Account -----------")
        receiver_address_str = "AmNHbk46L5ZaFH942mxDrunhUb34S8xRd7ygNnqaW5nqJDt5ugKD"
        receiver_address = herapy.Account.decode_address(receiver_address_str)
        print("  > Receiver Address: {}".format(receiver_address_str))
        print(''.join('{:d} '.format(x) for x in receiver_address))

        print("------ Deploy SC -----------")
        tx, result = aergo.deploy_sc(amount=0, payload=payload)
        print("  > TX: {}".format(tx.tx_hash_str))
        print("{}".format(herapy.convert_tx_to_json(tx)))
        if int(result['error_status']) != herapy.CommitStatus.TX_OK:
            print("    > ERROR[{0}]: {1}".format(result['error_status'], result['detail']))
        else:
            print("    > result : {}".format(result))
            print("      > result.hash : {}".format(base58.b58encode(result['hash'])))
            print(''.join('{:d} '.format(x) for x in tx.tx_hash))

        time.sleep(3)

        print("------ Check deployment of SC -----------")
        print("  > TX: {}".format(tx.tx_hash_str))
        sc_address, status, ret = aergo.get_tx_result(tx.tx_hash)
        if status != "CREATED":
            print("  > ERROR[{0}]:{1}: {2}".format(sc_address, status, ret))
            aergo.disconnect()
            return
        print("  > SC Address: {}".format(sc_address))

        print("------ Call SC -----------")
        tx, result = aergo.call_sc(sc_address, "setItem", args=["key1", "value1"])

        time.sleep(3)

        print("------ Check result of Call SC -----------")
        print("  > TX: {}".format(tx.tx_hash_str))
        sc_address, status, ret = aergo.get_tx_result(tx.tx_hash)
        if status != "SUCCESS":
            print("  > ERROR[{0}]:{1}: {2}".format(sc_address, status, ret))
            aergo.disconnect()
            return
        print("  > SC Address: {}".format(sc_address))

        print("------ Query SC -----------")
        result = aergo.query_sc(sc_address, "getItem", args=["key1"])

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except grpc.RpcError as e:
        print('Get Blockchain Status failed with {0}: {1}'.format(e.code(), e.details()))


if __name__ == '__main__':
    run()

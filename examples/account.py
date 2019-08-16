import sys
import traceback

import aergo.herapy as herapy
import hashlib


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print(*args, **kwargs)


def run():
    try:
        aergo = herapy.Aergo()

        aergo.new_account(skip_state=True)
        private_key_bytes = bytes(aergo.account.private_key)
        print("int(private key bytes) = {}".format(herapy.utils.bytes_to_int_str(private_key_bytes)))

        aergo.import_account(exported_data="MNxKz7jkvDGd61cifsmq2M21XL1uyvEcFS89BQpDMx57n44K3pfySoumSTdw7MS6HgfNy3ToJ7ravf", password="1234")
        private_key_bytes = bytes(aergo.account.private_key)
        signing_key = aergo.account.private_key.get_signing_key()
        verifying_key =  signing_key.get_verifying_key()
        print("to pem = {}".format(verifying_key.to_pem()))
        print("int(private key bytes) = {}".format(herapy.utils.bytes_to_int_str(private_key_bytes)))
        print("Address = {}".format(str(aergo.account.address)))

        pubkey_bytes_head = "\x08\x02\x12".encode("latin-1")
        print("int(public key bytes head) = {}".format(herapy.utils.bytes_to_int_str(pubkey_bytes_head)))

        print("Compress")
        pubkey_bytes = herapy.utils.convert_public_key_to_bytes(aergo.account.public_key)
        print("bytes(public key) = {}".format(pubkey_bytes))
        print("int(public key bytes) = {}".format(herapy.utils.bytes_to_int_str(pubkey_bytes)))

        p2p_pubkey_bytes = pubkey_bytes_head + len(pubkey_bytes).to_bytes(length=1, byteorder='big') + pubkey_bytes
        print("bytes(p2p public key) = {}".format(p2p_pubkey_bytes))
        print("int(p2p public key bytes) = {}".format(herapy.utils.bytes_to_int_str(p2p_pubkey_bytes)))
        pubkey_txt = herapy.utils.encode_b64(p2p_pubkey_bytes)
        print("p2p public key = {}".format(pubkey_txt))

        '''
        print("No compress")
        pubkey_bytes = herapy.utils.convert_public_key_to_bytes(aergo.account.public_key, compressed=False)
        print("bytes(public key) = {}".format(pubkey_bytes))
        pubkey_txt = herapy.utils.encode_b64(pubkey_bytes)
        print("public key = {}".format(pubkey_txt))
        '''

        print("generate ID")
        '''
        hash = hashlib.sha256()
        hash.update(p2p_pubkey_bytes)
        id_bytes = hash.digest()
        '''
        id_bytes = "\x00\x25".encode("latin-1") + p2p_pubkey_bytes
        print("int(id bytes) = {}".format(herapy.utils.bytes_to_int_str(id_bytes)))
        id = herapy.utils.encode_b58(id_bytes)
        print("id = {}".format(id))

        aergo.new_account(skip_state=True)
        pubkey_bytes = herapy.utils.convert_public_key_to_bytes(aergo.account.public_key)
        print("bytes(public key) = {}".format(pubkey_bytes))


        print("------ Connect AERGO -----------")
        aergo.connect('localhost:7845')

        print("------ Get Accounts without State in Node -----------")
        accounts = aergo.get_node_accounts(skip_state=True)
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo              = {}".format(account.balance.aergo))
            print("        + gaer               = {}".format(account.balance.gaer))
            print("        + aer                = {}".format(account.balance.aer))
            print("    - nonce                  = {}".format(account.nonce))
            print("    - code hash              = {}".format(account.code_hash))
            print("    - storage root           = {}".format(account.storage_root))
            print("    - sql recovery point     = {}".format(account.sql_recovery_point))

        print("------ Get Accounts in Node -----------")
        accounts = aergo.get_node_accounts()
        for i, account in enumerate(accounts):
            print("  > account state : {}".format(account))
            print("    - balance")
            print("        + aergo              = {}".format(account.balance.aergo))
            print("        + gaer               = {}".format(account.balance.gaer))
            print("        + aer                = {}".format(account.balance.aer))
            print("    - nonce                  = {}".format(account.nonce))
            print("    - code hash              = {}".format(account.code_hash))
            print("    - storage root           = {}".format(account.storage_root))
            print("    - sql recovery point     = {}".format(account.sql_recovery_point))

        print("------ Create Account -----------")
        account = aergo.new_account()

        print("Private Key      = {}".format(account.private_key))
        print("Public Key       = {}".format(account.public_key))
        print("Address          = {}".format(account.address))

        print("------ Get Account State -----------")
        aergo.get_account()
        print("  > account state in 'aergo'")
        print("    - balance")
        print("        + aergo              = {}".format(account.balance.aergo))
        print("        + gaer               = {}".format(account.balance.gaer))
        print("        + aer                = {}".format(account.balance.aer))
        print("    - nonce                  = {}".format(account.nonce))
        print("    - code hash              = {}".format(account.code_hash))
        print("    - storage root           = {}".format(account.storage_root))
        print("    - sql recovery point     = {}".format(account.sql_recovery_point))
        print(account)

        print("------ Get Configured Account -----------")
        accounts = [
            {
                "private_key": "eHoEcHnaxpGpgzknXjuwon8VFVrLkKHC4FckGuGkQ8depiDDfyUAWC3L",
                "address": "AmPZKCJpT98V9Tc8dBUbRg78M1jgoB1ZEh97Rs1r5KewPcCiURf7",
            },
        ]
        for i, account in enumerate(accounts):
            print("  [{}]".format(i))
            print("    > private key   : {}".format(account['private_key']))
            print("    > address       : {}".format(account['address']))

            # check account state
            a = aergo.get_account(address=account['address'])
            print("    > account state : {}".format(a))
            print("    - balance")
            print("        + aergo              = {}".format(a.balance.aergo))
            print("        + gaer               = {}".format(a.balance.gaer))
            print("        + aer                = {}".format(a.balance.aer))
            print("    - nonce                  = {}".format(a.nonce))
            print("    - code hash              = {}".format(a.code_hash))
            print("    - storage root           = {}".format(a.storage_root))
            print("    - sql recovery point     = {}".format(a.sql_recovery_point))

        print("------ Disconnect AERGO -----------")
        aergo.disconnect()
    except Exception as e:
        eprint(e)
        traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    run()

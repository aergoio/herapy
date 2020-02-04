import aergo.herapy as herapy
from aergo.herapy.account import Account
from aergo.herapy.utils.encryption import (
    encrypt_to_keystore_v1,
    decrypt_keystore_v1
)
from aergo.herapy.utils.converter import (
    privkey_to_address,
)


keystore = {
    "kdf": {
        "algorithm": "scrypt",
        "mac": "47006a8c1c17f56991ba412a4670da0c373f949ea64918531551e49fed0272ac",
        "params": {
            "dklen": 32,
            "n": 1024,
            "p": 1,
            "r": 8,
            "salt": "f8e0ba7b762bbff83ff7e48af13eedf08ce05fba29d247054139ca620357215f"
        }
    },
    "aergo_address": "AmM8Bspua3d1bACSzCaLUdstjooRLy1YqZ61Kk2nP4VfGTWJzDd6",
    "ks_version": "1",
    "cipher": {
        "algorithm": "aes-128-ctr",
        "ciphertext": "919b663b4039a9ea88470a6e7138acebb852820100360449e7457171ee003d08",
        "params": {
            "iv": "62fc13b3065a22ffd73804e23f47f690"
        }
    }
}


def test_account_keystore_v1():
    # create new account
    account1 = Account()
    privkey1 = bytes(account1.private_key)
    addr1 = bytes(account1.address)
    # encrypt to keystore
    keystore = Account.encrypt_to_keystore(account1, 'password', kdf_n=2**10)
    # decrypt keystore
    account2 = Account.decrypt_from_keystore(keystore, 'password')
    privkey2 = bytes(account2.private_key)
    addr2 = bytes(account2.address)
    # check the decrypted account is same with original one
    assert privkey1 == privkey2
    assert addr1 == addr2


def test_decrypt_keystore_v1():
    # check decrypted address matched the keystore address
    privkey_raw = decrypt_keystore_v1(keystore, 'password')
    address = privkey_to_address(privkey_raw)
    assert address == keystore['aergo_address']


def test_encrypt_keystore_v1():
    account = Account()
    privkey = bytes(account.private_key)
    address = str(account.address)
    new_keystore = encrypt_to_keystore_v1(
        privkey, address, 'password',  kdf_n=2**10)

    # check keystore format
    assert keystore['ks_version'] == new_keystore['ks_version']
    assert keystore['cipher']['algorithm'] == \
        new_keystore['cipher']['algorithm']
    assert keystore['kdf']['algorithm'] == new_keystore['kdf']['algorithm']


def test_aergo_import_export_account():
    hera = herapy.Aergo()
    account = hera.import_account_from_keystore(keystore, 'password', skip_state=True)
    assert str(account.address) == keystore['aergo_address']
    new_keystore = hera.export_account_to_keystore('password', kdf_n=2**10)
    assert new_keystore['aergo_address'] == keystore['aergo_address']

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.modes import CTR
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import hashlib
import os
import copy

from .converter import (
    privkey_to_address
)


KEYSTORE_V1 = {
    "aergo_address": "",
    "ks_version": "1",
    "cipher": {
        "algorithm": "aes-128-ctr",
        "params": {
            "iv": ""
        },
        "ciphertext": ""
    },
    "kdf": {
        "algorithm": "scrypt",
        "params": {
            "dklen": 32,
            "n": 262144,
            "p": 1,
            "r": 8,
            "salt": ""
        },
        "mac": ""
    }
}


def decrypt_keystore_v1(keystore, password):
    # check version and algorithm names
    assert keystore['ks_version'] == \
        KEYSTORE_V1['ks_version'], "Invalid keystore version"

    assert keystore['cipher']['algorithm'] == \
        KEYSTORE_V1['cipher']['algorithm'], "Invalid cipher algorithm"

    assert keystore['kdf']['algorithm'] == \
        KEYSTORE_V1['kdf']['algorithm'], "Invalid kdf algorithm"

    ct = bytes.fromhex(keystore['cipher']['ciphertext'])

    # derive cipher_key (used to decrypt cipher text) from password
    backend = default_backend()
    kdf_params = keystore['kdf']['params']
    cipher_key = derive_cipher_key(
        bytes.fromhex(kdf_params['salt']),
        kdf_params['dklen'],
        kdf_params['n'],
        kdf_params['r'],
        kdf_params['p'],
        backend,
        password
    )

    # check mac to make sure the cipher key is correct
    mac = hashlib.sha256(cipher_key[16:32] + ct).digest().hex()
    assert mac == keystore['kdf']['mac'], "Failed to verify mac"

    # decrypt cipher text to get private key bytes
    iv = bytes.fromhex(keystore['cipher']['params']['iv'])
    cipher = Cipher(AES(cipher_key[:16]), CTR(iv), backend=backend)
    decryptor = cipher.decryptor()
    privkey_raw = decryptor.update(ct) + decryptor.finalize()

    # check address matches private key
    address = privkey_to_address(privkey_raw)
    assert address == keystore['aergo_address'], "Failed to verify address"

    return privkey_raw


def encrypt_to_keystore_v1(privkey, address, password, kdf_n=2**18):
    assert address == \
        privkey_to_address(privkey), "address doesn't match privkey"
    backend = default_backend()

    # create random cipher_key (derived from password) to encrypt
    salt = os.urandom(16)
    cipher_key = derive_cipher_key(
        salt,
        32,
        kdf_n,
        8,  # RFC 7914 recommendation
        1,  # RFC 7914 recommendation
        backend, password
    )

    # encrypt privkey
    iv = os.urandom(16)
    cipher = Cipher(AES(cipher_key[:16]), CTR(iv), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(privkey) + encryptor.finalize()

    # calculate mac
    mac = hashlib.sha256(cipher_key[16:32] + ct).digest().hex()

    # create keystore dictionary (json)
    keystore = copy.deepcopy(KEYSTORE_V1)
    keystore['cipher']['params']['iv'] = iv.hex()
    keystore['cipher']['ciphertext'] = ct.hex()
    keystore['kdf']['params']['n'] = kdf_n
    keystore['kdf']['params']['salt'] = salt.hex()
    keystore['kdf']['mac'] = mac
    keystore['aergo_address'] = address
    return keystore


def derive_cipher_key(salt, l, n, r, p, backend, password):
    kdf = Scrypt(
        salt=salt,
        length=l,
        n=n,
        r=r,
        p=p,
        backend=backend
    )
    return kdf.derive(password.encode())


def encrypt_bytes(data, password):
    """
    https://cryptography.io/en/latest/hazmat/primitives/aead/
    :param data: bytes to encrypt
    :return: encrypted  data (bytes)
    """
    if isinstance(password, str):
        password = bytes(password, encoding='utf-8')

    m = hashlib.sha256()
    m.update(password)
    hash_pw = m.digest()

    m = hashlib.sha256()
    m.update(password)
    m.update(hash_pw)
    enc_key = m.digest()

    nonce = hash_pw[4:16]
    aesgcm = AESGCM(enc_key)
    return aesgcm.encrypt(nonce=nonce,
                          data=data,
                          associated_data=b'')


def decrypt_bytes(encrypted_bytes, password):
    """
    https://cryptography.io/en/latest/hazmat/primitives/aead/
    :param encrypted_bytes: encrypted data (bytes)
    :param password: to decrypt the exported bytes
    :return: decrypted bytes
    """
    if isinstance(password, str):
        password = password.encode('utf-8')

    m = hashlib.sha256()
    m.update(password)
    hash_pw = m.digest()

    m = hashlib.sha256()
    m.update(password)
    m.update(hash_pw)
    dec_key = m.digest()

    nonce = hash_pw[4:16]
    aesgcm = AESGCM(dec_key)
    dec_value = aesgcm.decrypt(nonce=nonce,
                               data=encrypted_bytes,
                               associated_data=b'')
    return dec_value

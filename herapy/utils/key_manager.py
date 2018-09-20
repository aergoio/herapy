""""
Crypto information:

Library: https://github.com/warner/python-ecdsa

Security (from the above page):
This library does not protect against timing attacks. Do not allow attackers to measure how long it takes you to
generate a keypair or sign a message. This library depends upon a strong source of random numbers.
Do not use it on a system where os.urandom() is weak.

Parameters from HeraJ (/core/util/src/main/java/hera/util/pki/ECDSAKey.java):
KEY_ALGORITHM = "ECDSA";
CURVE_NAME = "secp256k1";
SIGN_ALGORITHM = "SHA256WithECDSA";
MAC_ALGORITHM = "HmacSHA256";
"""

import hashlib
import ecdsa
import os

class KeyManager:
    def generate_and_save_keys(self, keyname):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        open(f"{keyname}.public.pem", "wb+").write(vk.to_pem())
        open(f"{keyname}.private.pem", "wb+").write(sk.to_pem())

    def delete_keys(self, keyname):
        os.remove(f"{keyname}.public.pem")
        os.remove(f"{keyname}.private.pem")

    def load_signing_key_from_file(self, keyname):
        sk = ecdsa.SigningKey.from_pem(open(f"{keyname}.private.pem").read())
        return sk
    
    def load_verifying_key_from_file(self, keyname):
        vk = ecdsa.VerifyingKey.from_pem(open(f"{keyname}.public.pem").read())
        return vk
    
    def sign_message(self, sk, message):
        return sk.sign(self.utf8(message), hashfunc=hashlib.sha256)
    
    def verify_message(self, vk, message, signature):
        return vk.verify(self.utf8(signature), self.utf8(message), hashfunc=hashlib.sha256)

    def utf8(self, o):
        if isinstance(o, str):
            return o.encode('utf-8')
        else:
            return o


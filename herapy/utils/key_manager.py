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
    def __init__(self, keyname=""):
        self.sk = None
        self.vk = None
        if keyname == "":
            self.generate_keys()
        else:
            self.load_keys(keyname)

    def generate_keys(self):
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.vk = self.sk.get_verifying_key()

    def save_keys(self, keyname):
        open(f"{keyname}.public.pem", "wb+").write(self.vk.to_pem())
        open(f"{keyname}.private.pem", "wb+").write(self.sk.to_pem())

    def load_keys(self, keyname):
        self.sk = ecdsa.SigningKey.from_pem(open(f"{keyname}.private.pem").read())
        self.vk = ecdsa.VerifyingKey.from_pem(open(f"{keyname}.public.pem").read())

    def delete_keys(self, keyname):
        os.remove(f"{keyname}.public.pem")
        os.remove(f"{keyname}.private.pem")

    def sign_message(self, message):
        return self.sk.sign(self.utf8(message), hashfunc=hashlib.sha256)
    
    def verify_message(self, message, signature):
        return self.vk.verify(self.utf8(signature), self.utf8(message), hashfunc=hashlib.sha256)

    def utf8(self, o):
        if isinstance(o, str):
            return o.encode('utf-8')
        else:
            return o
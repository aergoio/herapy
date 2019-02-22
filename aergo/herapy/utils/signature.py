import ecdsa
from ecdsa.util import number_to_string, string_to_number

import hashlib

from .encoding import decode_address


def canonicalize_int(n, order):
    b = number_to_string(n, order)
    if (b[0] & 80) != 0:
        b = bytes([0]) + b
    return b


def serialize_sig(r, s, order):
    half_order = order >> 1
    if s > half_order:
        s = order - s

    rb = canonicalize_int(r, order)
    sb = canonicalize_int(s, order)

    length = 4 + len(rb) + len(sb)
    b = b'\x30' + bytes([length])
    b += b'\x02' + bytes([len(rb)]) + rb
    b += b'\x02' + bytes([len(sb)]) + sb
    return b


def deserialize_sig(sig):
    idx = 0
    if b'\x30'[0] != sig[idx]:
        # TODO error handling
        return None, None

    idx += 1

    length = len(sig) - 2
    if length != sig[idx]:
        # TODO error handling
        return None, None

    idx += 1

    # check R bytes
    if b'\x02'[0] != sig[idx]:
        # TODO error handling
        return None, None

    idx += 1
    r_len = sig[idx]
    idx += 1
    rb = sig[idx:idx+r_len]
    idx += r_len

    # check S bytes
    if b'\x02'[0] != sig[idx]:
        # TODO error handling
        return None, None

    idx += 1
    s_len = sig[idx]
    idx += 1
    sb = sig[idx:idx+s_len]

    return string_to_number(rb), string_to_number(sb)


def uncompress_key(compressed_key_hex):
    """
    base source : https://stackoverflow.com/questions/43629265/deriving-an-ecdsa-uncompressed-public-key-from-a-compressed-one?rq=1
    The code from bitcointalk sometimes produces a hex string uncompressed key of uneven length.
    """
    curve = ecdsa.SECP256k1

    prefix = compressed_key_hex[0:2]
    x_hex = compressed_key_hex[2:66]
    x = int(x_hex, 16)
    p = curve.curve.p()

    y_square = (pow(x, 3, p)  + 7) % p
    y_square_square_root = pow(y_square, (p+1)//4, p)
    if ((prefix == "02" and y_square_square_root & 1) or
        (prefix == "03" and not y_square_square_root & 1)):
        y = (-y_square_square_root) % p
    else:
        y = y_square_square_root

    computed_y_hex = format(y, '064x')
    computed_uncompressed_key = "04" + x_hex + computed_y_hex

    return computed_uncompressed_key


def verify_sig(msg, sig, address):
    """
    Verify that the signature 'sig' of the message 'msg' was made by 'address')
    """
    # format signature
    r, s = deserialize_sig(sig)
    signature = ecdsa.ecdsa.Signature(r, s)

    # format message
    number = string_to_number(msg)

    # get uncompressed pubkey from Aergo address
    pubkey_compressed = decode_address(address).hex()
    pubkey_uncompressed = uncompress_key(pubkey_compressed)
    pubkey = bytes.fromhex(pubkey_uncompressed)[1:]

    # verify signature matches pubkey
    vk = ecdsa.VerifyingKey.from_string(pubkey,
                                        curve=ecdsa.SECP256k1,
                                        hashfunc=hashlib.sha256)
    return vk.pubkey.verifies(number, signature)

# -*- coding: utf-8 -*-

import hashlib
from .encoding import decode_root


def bit_is_set(bits, i):
    return bits[int(i/8)] & (1 << (7-i % 8)) != 0


def verify_inclusion(ap, root, key, value):
    """ verify_inclusion verifies the merkle proof 'ap' (audit path) that
    the key/value pair in included in the trie with root 'root'.
    """
    leaf_hash = hashlib.sha256(key + value + bytes([256-len(ap)])).digest()
    return root == verify_proof(ap, 0, key, leaf_hash)


def verify_inclusion_c(ap, height, bitmap, root, key, value):
    """ verify_inclusion verifies the compressed merkle proof 'ap' (audit path)
    that the key/value pair in included in the trie with root 'root'.
    """
    leaf_hash = hashlib.sha256(key + value + bytes([256-height])).digest()
    return root == verify_proof_c(bitmap, key, leaf_hash, ap, height, 0, 0)


def verify_proof(ap, key_index, key, leaf_hash):
    """ verify_proof recursively hashes the result with the proof nodes in the
    audit path 'ap'
    """
    if key_index == len(ap):
        return leaf_hash

    if bit_is_set(key, key_index):
        right = verify_proof(ap, key_index+1, key, leaf_hash)
        return hashlib.sha256(ap[len(ap)-key_index-1] + right).digest()
    left = verify_proof(ap, key_index+1, key, leaf_hash)
    return hashlib.sha256(left + ap[len(ap)-key_index-1]).digest()


def verify_proof_c(bitmap, key, leaf_hash, ap, length, key_index, ap_index):
    """ verify_proof_c recursively hashes the result with the proof nodes in
    the compressed audit path 'ap'
    """
    if key_index == length:
        return leaf_hash

    if bit_is_set(key, key_index):
        if bit_is_set(bitmap, length-key_index-1):
            right = verify_proof_c(bitmap, key, leaf_hash, ap, length,
                                   key_index+1, ap_index+1)
            return hashlib.sha256(ap[len(ap)-ap_index-1] + right).digest()
        left = verify_proof_c(bitmap, key, leaf_hash, ap, length,
                              key_index+1, ap_index)
        return hashlib.sha256(bytes([0]) + left).digest()

    if bit_is_set(bitmap, length-key_index-1):
        right = verify_proof_c(bitmap, key, leaf_hash, ap, length,
                               key_index+1, ap_index+1)
        return hashlib.sha256(right + ap[len(ap)-ap_index-1]).digest()
    left = verify_proof_c(bitmap, key, leaf_hash, ap, length,
                          key_index+1, ap_index)
    return hashlib.sha256(left + bytes([0])).digest()


def verify_exclusion(root, ap, key, proofKey, proofVal):
    """ verify_exclusion verifies the merkle proof that a default
    node (bytes([0]) is included on the path of the 'key', or that the
    proofKey/proofVal key pair is included on the path of the 'key'
    """
    if isinstance(root, str) and len(root) != 0:
        root = decode_root(root)

    if not proofKey:
        # return true if a DefaultLeaf in the key path is included in the trie
        return root == verify_proof(ap, 0, key, bytes([0]))

    # Check if another kv leaf is on the key path in 2 steps
    # 1- Check the proof leaf exists
    if not verify_inclusion(ap, root, proofKey, proofVal):
        # the proof leaf is not included in the trie
        return False

    # 2- Check the proof leaf is on the key path
    for b in range(len(ap)):
        if bit_is_set(key, b) != bit_is_set(proofKey, b):
            # the proofKey leaf node is not on the path of the key
            return False
    # return true because we verified proofKey/proofVal is on the key path
    return True


def verify_exclusion_c(root, ap, length, bitmap, key, proofKey, proofVal):
    """ verify_exclusion_c verifies the compressed merkle proof that a default
    node (bytes([0]) is included on the path of the 'key', or that the
    proofKey/proofVal key pair is included on the path of the 'key'
    """
    if isinstance(root, str) and len(root) != 0:
        root = decode_root(root)

    if not proofKey:
        # return true if a DefaultLeaf in the key path is included in the trie
        return root == verify_proof_c(bitmap, key, bytes([0]), ap,
                                      length, 0, 0)

    # Check if another kv leaf is on the key path in 2 steps
    # 1- Check the proof leaf exists
    if not verify_inclusion_c(ap, length, bitmap, root, proofKey, proofVal):
        # the proof leaf is not included in the trie
        return False

    # 2- Check the proof leaf is on the key path
    for b in range(length):
        if bit_is_set(key, b) != bit_is_set(proofKey, b):
            # the proofKey leaf node is not on the path of the key
            return False
    # return true because we verified proofKey/proofVal is on the key path
    return True

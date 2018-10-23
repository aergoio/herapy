import hashlib

from herapy import transaction
from herapy.utils.encoding import encode_address, encode_hash, encode_signature

def tx_to_transaction(tx):
    return transaction.Transaction(
        hash=encode_hash(tx.hash),
        nonce=tx.body.nonce,
        from_address=encode_address(tx.body.account),
        to_address=encode_address(tx.body.recipient),
        amount=tx.body.amount,
        payload=tx.body.payload,
        signature=encode_signature(tx.body.sign),
        type=tx.body.type)

def calculate_tx_hash(tx):
    m = hashlib.sha256()
    tx_bytes = tx.body.nonce.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.account)
    m.update(tx.body.recipient)
    tx_bytes = tx.body.amount.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.payload)
    tx_bytes = tx.body.limit.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    tx_bytes = tx.body.price.to_bytes(8, byteorder='little')
    m.update(tx_bytes)
    tx_bytes = tx.body.type.to_bytes(4, byteorder='little')
    m.update(tx_bytes)
    m.update(tx.body.sign)
    return m.digest()

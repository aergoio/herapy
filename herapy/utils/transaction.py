from herapy.transaction import transaction
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

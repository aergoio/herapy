import grpc
import base58

# TODO: refactor these to use package imports when grpc working
import account_pb2
import blockchain_pb2

import rpc_pb2
import rpc_pb2_grpc

from herapy.utils.encoding import encode_address, decode_address, encode_hash, decode_hash
from herapy.utils.transaction import tx_to_transaction
from herapy.transaction import transaction


class Rpc:
    def __init__(self, channel):
        channel = grpc.insecure_channel(channel)
        self.rpc = rpc_pb2_grpc.AergoRPCServiceStub(channel)
        self.empty = rpc_pb2.Empty()

    # Accounts
    def create_account(self, passphrase):
        personal = rpc_pb2.Personal()
        personal.passphrase = passphrase
        account = self.rpc.CreateAccount(personal)
        return encode_address(account.address)


    def get_accounts(self):
        accounts = self.rpc.GetAccounts(self.empty).accounts
        addresses = [encode_address(account.address) for account in accounts]
        return addresses


    def lock(self, address, passphrase):
        personal = self._personal_with_address_and_passphrase(address, passphrase)
        address = self.rpc.LockAccount(personal).address
        return encode_address(address)


    def unlock(self, address, passphrase):
        personal = self._personal_with_address_and_passphrase(address, passphrase)
        address = self.rpc.UnlockAccount(personal).address
        return encode_address(address)


    def send_transaction(self, tx):
        tx_body = blockchain_pb2.TxBody()

        tx_body.account = decode_address(tx.from_address)
        tx_body.recipient = decode_address(tx.to_address)
        tx_body.amount = tx.amount
        tx_body.payload = tx.payload
        tx_body.type = tx.type
        tx = blockchain_pb2.Tx()

        tx.body.CopyFrom(tx_body)

        hash = self.rpc.SendTX(tx).hash
        return encode_hash(hash)


    def sign_transaction(self, tx):
        tx_body = blockchain_pb2.TxBody()

        tx_body.nonce = tx.nonce
        tx_body.account = decode_address(tx.from_address)
        tx_body.recipient = decode_address(tx.to_address)
        tx_body.amount = tx.amount
        tx_body.payload = tx.payload
        tx_body.type = tx.type

        tx = blockchain_pb2.Tx()
        tx.body.CopyFrom(tx_body)

        signed_tx = self.rpc.SignTX(tx)
        return tx_to_transaction(signed_tx)

    def _personal_with_address_and_passphrase(self, address, passphrase):
        account = account_pb2.Account()
        account.address = decode_address(address)

        personal = rpc_pb2.Personal() # !!! TODO this creates a new Personal() each time??? but this is what HeraJS does???
        personal.passphrase = passphrase
        personal.account.CopyFrom(account)

        return personal

    # Client
    def is_connected(self):
        return False # really?



    def node_state(self):
        return self.rpc.NodeState(rpc_pb2.SingleBytes())


    def blockchain(self):
        return self.rpc.Blockchain(self.empty)

    def list_block_headers(self):
        pass

    def get_peers(self):
        return self.rpc.GetPeers(self.empty)



rpc = Rpc('localhost:7845')
account = rpc.create_account('123')
account2 = rpc.create_account('456')
unlocked = rpc.unlock(account, '123')
tx = transaction.Transaction(from_address=unlocked,
                             nonce=0,
                             hash=0,
                             to_address=account2,
                             amount=0,
                             payload=b'',
                             signature=b'',
                             type=0)
print(vars(rpc.sign_transaction(tx)))
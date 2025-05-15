# transaction.py
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Transaction:
    def __init__(self, sender, recipient, amount, fee=0, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee
        }

    def sign_transaction(self, private_key):
        signer = pkcs1_15.new(RSA.import_key(private_key))
        hashed = SHA256.new(json.dumps(self.to_dict(), sort_keys=True).encode())
        self.signature = signer.sign(hashed).hex()

    def is_valid(self):
        if self.sender == "MINING":
            return True  # Skip for mining rewards

        try:
            pub_key = RSA.import_key(self.sender.encode())
            verifier = pkcs1_15.new(pub_key)
            hashed = SHA256.new(json.dumps(self.to_dict(), sort_keys=True).encode())
            verifier.verify(hashed, bytes.fromhex(self.signature))
            return True
        except (ValueError, TypeError):
            return False

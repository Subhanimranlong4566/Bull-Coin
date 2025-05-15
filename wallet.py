# wallet.py
from Crypto.PublicKey import RSA

class Wallet:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.private_key = self.key.export_key().decode()
        self.public_key = self.key.publickey().export_key().decode()

    def get_address(self):
        return self.public_key

    def save_keys(self, path='wallet'):
        with open(f"{path}_private.pem", "w") as f:
            f.write(self.private_key)
        with open(f"{path}_public.pem", "w") as f:
            f.write(self.public_key)

    @staticmethod
    def load_keys(path='wallet'):
        with open(f"{path}_private.pem", "r") as f:
            private_key = f.read()
        with open(f"{path}_public.pem", "r") as f:
            public_key = f.read()
        wallet = Wallet()
        wallet.private_key = private_key
        wallet.public_key = public_key
        wallet.key = RSA.import_key(private_key)
        return wallet

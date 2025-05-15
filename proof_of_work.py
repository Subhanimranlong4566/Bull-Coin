# proof_of_work.py
import hashlib
import time
import logging

class ProofOfWork:
    def __init__(self, blockchain, difficulty=4):
        self.blockchain = blockchain
        self.difficulty = difficulty
        self.target = '0' * difficulty  # The target to mine for (e.g., '0000' for difficulty 4)

    def mine_block(self, block):
        """ Perform Proof of Work by finding a valid nonce for the block """
        block.nonce = 0
        block.hash = self.calculate_hash(block)
        logging.info(f"Mining block {block.index}...")

        # Iterate until we find a hash that satisfies the difficulty level
        while not block.hash.startswith(self.target):
            block.nonce += 1
            block.hash = self.calculate_hash(block)
        
        logging.info(f"Block mined: {block.hash}")
        return block

    def calculate_hash(self, block):
        """ Calculate the hash for a block using its properties (Index, Timestamp, Transactions, Nonce) """
        block_string = f"{block.index}{block.timestamp}{block.transactions}{block.previous_hash}{block.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def validate_block(self, block):
        """ Validate that the block's hash matches the Proof of Work criteria """
        return block.hash.startswith(self.target)

    def mine(self):
        """ Mine a new block and add it to the blockchain """
        new_block = self.blockchain.create_new_block()
        mined_block = self.mine_block(new_block)
        self.blockchain.add_block(mined_block)
        return mined_block

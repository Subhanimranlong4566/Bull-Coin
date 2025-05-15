# blockchain.py
import time
import json
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self, difficulty=2, mining_reward=50):
        self.unconfirmed_transactions = []  # mempool
        self.chain = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.nodes = set()  # for P2P
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.is_valid():
            return False
        self.unconfirmed_transactions.append(transaction)
        return True

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine_pending_transactions(self, miner_address):
        # Add mining reward as a special transaction
        reward_tx = Transaction("MINING", miner_address, self.mining_reward)
        self.unconfirmed_transactions.append(reward_tx)

        # Sort by fee (optional)
        self.unconfirmed_transactions.sort(key=lambda tx: tx.fee, reverse=True)

        block = Block(
            index=len(self.chain),
            transactions=[tx.__dict__ for tx in self.unconfirmed_transactions],
            timestamp=time.time(),
            previous_hash=self.get_last_block().compute_hash()
        )

        proof = self.proof_of_work(block)
        block.hash = proof
        self.chain.append(block)
        self.unconfirmed_transactions = []
        return block

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]
            if current['previous_hash'] != Block(**previous).compute_hash():
                return False
            if not Block(**current).compute_hash().startswith('0' * self.difficulty):
                return False
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx['sender'] == address:
                    balance -= tx['amount'] + tx.get('fee', 0)
                if tx['recipient'] == address:
                    balance += tx['amount']
                if tx.get('fee', 0) and tx['sender'] != "MINING" and tx['recipient'] != address:
                    # Fees should go to miner, not double counted
                    continue
        return balance

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = [Block(**blk) for blk in new_chain]
            return True
        return False

# consensus.py
import logging

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def resolve_conflict(self):
        """
        Resolves conflicts in the blockchain by comparing the lengths of two chains.
        The chain with the most blocks is considered the valid chain.
        """
        logging.info("Resolving conflict...")

        # Fetch all the nodes in the network (assumed to be connected via P2P)
        longest_chain = None

        # Compare the length of the chains of the current node and other nodes
        for node in self.blockchain.nodes:
            chain_length = len(node.get_chain())  # Get the length of the chain from the node

            # If a longer chain is found, replace the current longest chain
            if longest_chain is None or chain_length > len(longest_chain):
                longest_chain = node.get_chain()

        if longest_chain:
            logging.info(f"New longest chain found with {len(longest_chain)} blocks.")
            self.blockchain.chain = longest_chain  # Replace the current chain with the longest one
            return True  # A conflict was resolved
        return False  # No conflict

    def validate_chain(self):
        """
        Validates the entire chain for correctness (i.e., each block points to the correct previous block).
        """
        for i in range(1, len(self.blockchain.chain)):
            previous_block = self.blockchain.chain[i - 1]
            current_block = self.blockchain.chain[i]
            
            # Ensure that each block points to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                logging.error(f"Invalid block: {current_block.index} does not link correctly to previous block.")
                return False
        
        logging.info("Blockchain is valid.")
        return True

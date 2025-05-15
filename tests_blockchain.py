# tests_blockchain.py
import unittest
from blockchain import Blockchain
from block import Block
from wallet import Wallet
from p2p import P2PNetwork

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """ Set up a new blockchain and p2p network for each test """
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.p2p_network = P2PNetwork(self.blockchain)

    def test_create_block(self):
        """ Test block creation and addition to blockchain """
        self.blockchain.add_block({"transactions": []})
        self.assertEqual(len(self.blockchain.chain), 2, "Block was not added correctly")

    def test_transaction(self):
        """ Test adding a transaction to the blockchain """
        transaction = {"sender": "Alice", "receiver": "Bob", "amount": 100}
        self.blockchain.add_transaction(transaction)
        self.assertEqual(len(self.blockchain.pending_transactions), 1, "Transaction not added correctly")

    def test_mine_block(self):
        """ Test mining a block and adding it to the blockchain """
        self.blockchain.add_transaction({"sender": "Alice", "receiver": "Bob", "amount": 100})
        mined_block = self.blockchain.mine_block()
        self.assertEqual(len(self.blockchain.chain), 2, "Mining did not work correctly")
        self.assertEqual(mined_block['previous_hash'], self.blockchain.chain[-1]['hash'], "Incorrect previous hash")

    def test_p2p_add_node(self):
        """ Test adding a node to the P2P network """
        self.p2p_network.add_node_to_network("localhost:5001")
        self.assertIn("localhost:5001", self.p2p_network.nodes, "Node was not added to P2P network")

    def test_broadcast_block(self):
        """ Test broadcasting a block to other nodes in the network """
        block = {"index": 1, "transactions": [], "previous_hash": "0", "hash": "abc123"}
        self.p2p_network.broadcast_new_block(block)
        # You would implement actual broadcasting logic and mock the requests in a more complex test

    def test_sync_chain(self):
        """ Test syncing the blockchain with another node's chain """
        other_chain = [{"index": 0, "transactions": [], "previous_hash": "0", "hash": "genesis"}]
        self.blockchain.chain = other_chain  # Simulate receiving a shorter chain
        self.p2p_network.sync_chain()
        self.assertEqual(len(self.blockchain.chain), len(other_chain), "Chain synchronization did not work correctly")

    def test_validate_chain(self):
        """ Test chain validation logic """
        self.blockchain.add_block({"transactions": []})
        self.assertTrue(self.blockchain.validate_chain(), "Chain validation failed")

if __name__ == "__main__":
    unittest.main()

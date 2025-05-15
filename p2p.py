# p2p.py
import time 
import json
import logging
import threading
import requests
from flask import Flask, request
from flask_socketio import SocketIO, emit
from blockchain import Blockchain

class P2PNetwork:
    def __init__(self, blockchain, host="localhost", port=5000):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.nodes = set()
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

    def start_server(self):
        """ Start the Flask server for handling P2P communication """
        @self.app.route("/add_node", methods=["POST"])
        def add_node():
            data = request.get_json()
            node_address = data["node"]
            self.add_node_to_network(node_address)
            return "Node added!", 200

        @self.app.route("/get_chain", methods=["GET"])
        def get_chain():
            return json.dumps(self.blockchain.chain), 200

        @self.app.route("/add_block", methods=["POST"])
        def add_block():
            block_data = request.get_json()
            block = self.blockchain.add_block(block_data)
            return json.dumps(block), 200

        self.socketio.run(self.app, host=self.host, port=self.port)

    def add_node_to_network(self, node_address):
        """ Add a new node to the P2P network """
        self.nodes.add(node_address)
        logging.info(f"Node {node_address} added to the network.")

    def broadcast_new_block(self, block):
        """ Broadcast a newly mined block to all other nodes """
        for node in self.nodes:
            try:
                response = requests.post(f"http://{node}/add_block", json=block)
                if response.status_code == 200:
                    logging.info(f"Broadcasted block to {node}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error broadcasting block to {node}: {e}")

    def sync_chain(self):
        """ Sync the blockchain with other nodes """
        for node in self.nodes:
            try:
                response = requests.get(f"http://{node}/get_chain")
                if response.status_code == 200:
                    node_chain = response.json()
                    if len(node_chain) > len(self.blockchain.chain):
                        logging.info(f"Found longer chain from node {node}. Syncing...")
                        self.blockchain.chain = node_chain
            except requests.exceptions.RequestException as e:
                logging.error(f"Error syncing chain with {node}: {e}")

    def listen_for_new_transactions(self):
        """ Listen for new transactions from other nodes via socket.io """
        @self.socketio.on("new_transaction")
        def handle_new_transaction(transaction):
            self.blockchain.add_transaction(transaction)
            logging.info(f"New transaction received: {transaction}")
            self.broadcast_new_transaction(transaction)

    def broadcast_new_transaction(self, transaction):
        """ Broadcast new transaction to other nodes """
        for node in self.nodes:
            try:
                self.socketio.emit("new_transaction", transaction, room=node)
            except Exception as e:
                logging.error(f"Error broadcasting transaction to {node}: {e}")

    def start_sync_thread(self):
        """ Start a thread to sync with other nodes periodically """
        def sync_periodically():
            while True:
                self.sync_chain()
                time.sleep(60)  # Sync every 60 seconds

        sync_thread = threading.Thread(target=sync_periodically)
        sync_thread.daemon = True
        sync_thread.start()

# app.py
from flask import Flask, jsonify, request
from blockchain import Blockchain
from wallet import Wallet
from transaction import Transaction
import json

app = Flask(__name__)

# Initialize the Blockchain
blockchain = Blockchain()

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain = []
    for block in blockchain.chain:
        chain.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        })
    return jsonify({'chain': chain, 'length': len(blockchain.chain)})

@app.route('/transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount', 'private_key']

    if not all(field in values for field in required_fields):
        return 'Missing values', 400

    # Sign the transaction
    sender_private_key = values['private_key']
    transaction = Transaction(values['sender'], values['recipient'], values['amount'])
    transaction.sign_transaction(sender_private_key)

    if blockchain.add_transaction(transaction):
        return jsonify({"message": "Transaction added to the pool!"}), 201
    return 'Invalid transaction', 400

@app.route('/mine', methods=['GET'])
def mine():
    miner_wallet = Wallet()
    block = blockchain.mine_pending_transactions(miner_wallet.get_address())

    return jsonify({
        'message': 'Block mined successfully!',
        'block': {
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        }
    })

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

@app.route('/register_node', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.nodes.add(node)
    return jsonify({'message': 'New nodes have been added'}), 201

@app.route('/resolve_conflicts', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.replace_chain(blockchain.chain)
    if replaced:
        return jsonify({'message': 'Our chain was replaced with the longest chain.'})
    else:
        return jsonify({'message': 'Our chain is the longest chain.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

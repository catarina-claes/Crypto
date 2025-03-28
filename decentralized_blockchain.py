from flask import Flask, request, jsonify
import hashlib
import time
import json
import requests

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{json.dumps(self.transactions)}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(data).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 4  # seharusnya kesulitan ditentukan dari kesulitan blok sblmnya
        self.nodes = set()  # Menyimpan daftar node dalam jaringan

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def add_block(self, new_block):
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def create_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return False

        new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions, time.time())
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def register_node(self, address):
        self.nodes.add(address)

    def resolve_conflicts(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f"{node}/chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    def is_valid_chain(self, chain):
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            if current["previous_hash"] != previous["hash"]:
                return False
        return True

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    success = blockchain.mine_pending_transactions()
    if success:
        return jsonify({"message": "Mining successful"}), 200
    return jsonify({"message": "No transactions to mine"}), 400

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    blockchain.create_transaction(data["sender"], data["recipient"], data["amount"])
    return jsonify({"message": "Transaction added"}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chain": [block.__dict__ for block in blockchain.chain],
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    data = request.get_json()
    for node in data["nodes"]:
        blockchain.register_node(node)
    return jsonify({"message": "Nodes registered successfully"}), 201

@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return jsonify({"message": "Chain replaced"}), 200
    return jsonify({"message": "Chain is authoritative"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

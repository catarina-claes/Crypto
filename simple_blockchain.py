import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(data).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # Ubah untuk kontrol kesulitan mining

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", time.time())

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, transactions, time.time())
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Contoh penggunaan
blockchain = Blockchain()
blockchain.add_block("Alice mengirim 10 Coin ke Bob")
blockchain.add_block("Bob mengirim 5 Coin ke Charlie")

for block in blockchain.chain:
    print(f"Index: {block.index}, Hash: {block.hash}, Transactions: {block.transactions}")

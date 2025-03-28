import requests
import hashlib
import time

# Ambil data blockchain dari Blockstream API
BLOCKSTREAM_API = "https://blockstream.info/api"

def get_latest_block():
    """Ambil blok terbaru dari Bitcoin blockchain"""
    latest_height = requests.get(f"{BLOCKSTREAM_API}/blocks/tip/height").text
    latest_hash = requests.get(f"{BLOCKSTREAM_API}/block-height/{latest_height}").text
    mempool = requests.get(f"{BLOCKSTREAM_API}/mempool/recent").text
    difficulty = requests.get(f"https://blockchain.info/q/getdifficulty").text
    return latest_height, latest_hash, mempool, difficulty

def calculate_merkle_root(transactions):
    """Simulasi perhitungan Merkle Root (hash dari semua transaksi)"""
    if not transactions:
        return "0" * 64  # Jika tidak ada transaksi, isi dengan hash kosong

    hashes = [hashlib.sha256(tx.encode()).hexdigest() for tx in transactions]
    
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])  # Duplikasi jika jumlah ganjil
        hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                  for i in range(0, len(hashes), 2)]
    
    return hashes[0]

def mine_block(previous_hash, mempool, difficulty):
    """Melakukan mining dengan mencari nonce yang sesuai"""
    version = "00000020"
    nonce = 0
    start_time = time.time()
    merkle_root = calculate_merkle_root(mempool) # Ini harusnya seluruh transaksinya deh.. bukan mempoolnya..
    timestamp = int(time.time())  # Ini timestamp harusnya dari block sblmnya?
    difficulty_target = "0" * difficulty  # Target hash dengan nol di depan

    while True:
        block_header = f"{version}{previous_hash}{merkle_root}{timestamp}{difficulty}{nonce}"
        block_hash = hashlib.sha256(hashlib.sha256(block_header.encode()).digest()).hexdigest()

        if block_hash[:difficulty] == difficulty_target:
            end_time = time.time()
            print(f"Block mined! 🎉\nNonce: {nonce}\nHash: {block_hash}\nTime: {end_time - start_time:.2f} sec")
            return nonce, block_hash

        nonce += 1

# Dapatkan blok terbaru dan mulai mining
height, previous_hash, mempool, difficulty = get_latest_block()
print(height)
print(previous_hash)
print(calculate_merkle_root(mempool))
print(difficulty)

difficulty_sim = 5  # Bitcoin asli jauh lebih tinggi (10^14), ini hanya simulasi

print(f"Mining block after {height} with previous hash {previous_hash}...")
mine_block(previous_hash, mempool, difficulty_sim)

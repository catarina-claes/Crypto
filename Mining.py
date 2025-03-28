import hashlib
import time

# Simulasi blok dengan data sederhana
def mine_block(previous_hash, transactions, difficulty):
    nonce = 0
    start_time = time.time()

    while True:
        block_data = f"{previous_hash}{transactions}{nonce}".encode()
        block_hash = hashlib.sha256(block_data).hexdigest()

        # Cek apakah hash memenuhi syarat (jumlah nol di awal sesuai difficulty)
        if block_hash[:difficulty] == "0" * difficulty:
            end_time = time.time()
            print(f"Blok ditemukan! ⛏️")
            print(f"Hash: {block_hash}")
            print(f"Nonce: {nonce}")
            print(f"Waktu yang dibutuhkan: {end_time - start_time:.2f} detik")
            return block_hash

        nonce += 1

# Contoh transaksi
previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
transactions = "Alice mengirim 1 BTC ke Bob"
difficulty = 7  # Semakin besar, semakin sulit

# Jalankan mining simulasi
mine_block(previous_hash, transactions, difficulty)

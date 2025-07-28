import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_inventaris (
            id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pelanggan TEXT,
            status_pelanggan TEXT,
            list_barang TEXT,
            jenis_transaksi TEXT,
            jumlah INTEGER,
            metode_pembayaran TEXT,
            tanggal_order TEXT,
            tanggal_kembali TEXT,
            total INTEGER
        );
    """)
    conn.commit()
    conn.close()
    print("Database & tabel inventaris siap!")

if __name__ == "__main__":
    setup_database()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'inventaris_pcc.db'
DB_PATH = os.path.join(BASE_DIR, 'data', NAMA_DB)

# Daftar barang + harga (update sesuai tabel yang kamu upload)
DAFTAR_BARANG = {
    "Papan nama Akrilik (25cm)": 2000,
    "Papan nama Akrilik (30cm)": 3000,
    "Bendera Merah Putih": 3000,
    "Tampah": 3000,
    "Piring": 2000,
    "Galon": 2000,
    "Pompa Galon": 2000,
    "Kain Dekor": 10000,
    "Taplak Meja": 2000,
    "Teko": 3000,
    "Tempat Tisu (Plastik)": 2000,
    "Tempat Tisu (Kayu)": 3000,
    "Vas Bunga": 2000,
    "Mic Wireless (Biru)": 15000,
    "Mic Wireless (Coklat)": 20000,
    "Nampan": 2000,
    "MMT Bekas": 5000,
    "Tikar": 5000,
    "Palu Sidang": 8000,
    "Rol Kabel (Bulat)": 8000,
    "Rol Kabel (Kotak)": 3000
}

METODE_PEMBAYARAN = ["Tunai", "Transfer", "E-Wallet"]
STATUS_PELANGGAN = ["Mahasiswa", "Ormawa", "Umum"]
JENIS_TRANSAKSI = ["Peminjaman", "Pembelian"]

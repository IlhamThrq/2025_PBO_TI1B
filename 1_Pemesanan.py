import streamlit as st
import datetime
import urllib.parse
from konfigurasi import DAFTAR_BARANG, METODE_PEMBAYARAN, STATUS_PELANGGAN, JENIS_TRANSAKSI
from manajer_order import ManajerOrderInventaris
from model import OrderInventaris

st.set_page_config(page_title="Pemesanan | Polytechnic Computer Club", page_icon="📝")

# Judul Utama
st.markdown(
    """
    <h1 style='font-size:2.3rem; margin-bottom: 0.2em; color:#f7b731;'>
        <span style="vertical-align:middle;">🖥️</span> Polytechnic Computer Club
    </h1>
    """,
    unsafe_allow_html=True
)

# Header Formulir di dalam “tabel” sederhana
st.markdown(
    """
    <table style='background:#f1f2f6;border-radius:10px;width:100%;margin-bottom:1.5em;'>
      <tr>
        <td style='font-size:1.3rem;font-weight:bold;color:#374151;padding:12px 8px;'>
          📋 Formulir Pemesanan
        </td>
      </tr>
    </table>
    """,
    unsafe_allow_html=True
)
manajer = ManajerOrderInventaris()

with st.form("form_pemesanan"):
    nama = st.text_input("Nama Pelanggan*", "")
    status = st.selectbox("Status Pelanggan*", ["-- Pilih --"] + STATUS_PELANGGAN)
    jenis_transaksi = st.selectbox("Jenis Transaksi*", ["-- Pilih --"] + JENIS_TRANSAKSI)
    list_barang = st.multiselect("Pilih Barang*", list(DAFTAR_BARANG.keys()))
    jumlah = st.number_input(
        "Jumlah (per barang, misal ambil 3 jenis barang dan jumlah=2 maka total barang=6)",
        min_value=1, value=1
    )
    metode = st.selectbox("Metode Pembayaran*", ["-- Pilih --"] + METODE_PEMBAYARAN)
    tanggal_order = st.date_input("Tanggal Pemesanan/Peminjaman*", datetime.date.today())
    tanggal_kembali = st.date_input(
        "Tanggal Pengembalian",
        datetime.date.today(),
        help="Hanya wajib diisi untuk transaksi peminjaman. Untuk pembelian/perawatan, boleh diabaikan."
    )

    # Kalkulasi total harga otomatis
    if list_barang:
        total_harga = sum(DAFTAR_BARANG[nama] for nama in list_barang) * jumlah
    else:
        total_harga = 0

    st.info("Harga satuan: " + ", ".join([f"{b} (Rp{DAFTAR_BARANG[b]:,})" for b in list_barang]) if list_barang else "Pilih barang untuk lihat harga.")
    st.success(f"Total harga otomatis: Rp {total_harga:,}")

    submit = st.form_submit_button("Ajukan Pesanan")

if submit:
    if (not nama
        or not list_barang
        or status == "-- Pilih --"
        or jenis_transaksi == "-- Pilih --"
        or metode == "-- Pilih --"):
        st.error("❌ Lengkapi semua field bertanda *.")
    else:
        # Jika bukan peminjaman, tanggal_kembali dianggap None/empty
        tgl_kembali_value = tanggal_kembali if jenis_transaksi == "Peminjaman" else None
        order = OrderInventaris(
            nama_pelanggan=nama,
            status_pelanggan=status,
            list_barang=list_barang,
            jenis_transaksi=jenis_transaksi,
            jumlah=jumlah,
            metode_pembayaran=metode,
            tanggal_order=tanggal_order,
            tanggal_kembali=tgl_kembali_value,
            total=total_harga
        )
        if manajer.tambah_order(order):
            st.success("Pesanan berhasil diajukan!")
            st.balloons()
            
            # ====== BAGIAN LINK WA OTOMATIS DINAMIS ======
            no_wa = "6285291905080"  # ganti dengan nomor adminmu!
            detail_barang = "\n".join([f"- {b} x {jumlah}" for b in list_barang])
            if jenis_transaksi == "Peminjaman":
                periode = f"{tanggal_order} s.d. {tanggal_kembali}"
            else:
                periode = f"{tanggal_order}"
            pesan = (
                f"Halo admin, saya {nama} ({status}) ingin melakukan {jenis_transaksi.upper()} "
                f"barang berikut:\n{detail_barang}\nTanggal: {periode}\n"
                f"Total pembayaran: Rp{total_harga:,}"
            )
            wa_link = f"https://wa.me/{no_wa}?text={urllib.parse.quote(pesan)}"
            st.markdown(
                f"""
                <a href="{wa_link}" target="_blank" style="background:#25d366;color:white;padding:10px 18px;
                border-radius:5px;text-decoration:none;display:inline-block;font-weight:bold;">
                📱 Kirim konfirmasi ke Admin via WhatsApp
                </a>
                """,
                unsafe_allow_html=True
            )
            # ====== END LINK WA ======
        else:
            st.error("Gagal menyimpan pesanan.")

import streamlit as st
from datetime import datetime
import urllib.parse

def main():
    st.set_page_config(page_title="Beranda PCC Store", page_icon="🏪", layout="wide")

    st.title("👋 Selamat Datang di Aplikasi PCC Store Inventaris")
    st.markdown(
        """
        <div style='background: #223a6a; color: #fff; padding: 16px; border-radius: 10px; text-align:center; margin-bottom: 20px;'>
            <b>PCC Store</b> menyediakan berbagai keperluan barang inventaris kebutuhan mahasiswa.<br>
            <i>Peminjaman, Pembelian, dan Maintenance barang UKM.</i>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("## 🚀 Fitur Utama")
    st.markdown("""
    - 📝 **Pemesanan/Peminjaman/Pembelian/Perawatan Barang**
    - 🗃️ **Riwayat Order (Khusus Admin)**
    - 📊 **Statistik Pendapatan (Khusus Admin)**
    """)

    st.markdown("## 📋 Cara Menggunakan")
    st.markdown("""
    1. Pilih menu **Pemesanan** di sidebar.
    2. Isi detail pemesanan/peminjaman barang.
    3. Lakukan pembayaran jika pembelian/maintenance.
    4. Pantau status pesanan via kontak admin atau login panel.
    """)

    st.markdown("---")
    st.markdown(f"🕒 Akses terakhir: `{datetime.now().strftime('%d %B %Y %H:%M:%S')}`")

    # ====== KONTAK WA DINAMIS ======
    no_wa = "6285291905080"  # Ganti dengan nomor adminmu
    template_pesan = "Halo admin, saya ingin bertanya tentang inventaris PCC Store."
    wa_link = f"https://wa.me/{no_wa}?text={urllib.parse.quote(template_pesan)}"
    st.markdown("### 📞 Kontak")
    st.markdown(
        f"""
        <a href="{wa_link}" target="_blank" style="background:#25d366;color:white;padding:10px 18px;
        border-radius:5px;text-decoration:none;display:inline-block;font-weight:bold;">
        📱 Chat Admin via WhatsApp
        </a>
        """,
        unsafe_allow_html=True
    )
    # Kontak Instagram
    st.markdown(
        '<a href="https://www.instagram.com/pccstore/" target="_blank" style="background:#E4405F;color:white;padding:10px 18px;'
        'border-radius:5px;text-decoration:none;display:inline-block;font-weight:bold;">'
        '📸 Kunjungi Instagram PCC Store'
        '</a>',
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()

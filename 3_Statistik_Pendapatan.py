import streamlit as st
import pandas as pd
from datetime import datetime
from manajer_order import ManajerOrderInventaris
from admin_auth import AdminAuthenticator

def main():
    st.set_page_config(
        page_title="Statistik Pendapatan",
        page_icon="📊",
        layout="wide"
    )

    auth = AdminAuthenticator()
    auth.login_sidebar(key_prefix="statistik")
    if not auth.is_logged_in():
        st.error("❌ Halaman ini hanya untuk admin.")
        st.stop()

    st.title("📊 Statistik Pendapatan")
    st.caption(f"Hai, admin *{auth.get_username()}*!")

    manajer = ManajerOrderInventaris()
    df = manajer.get_dataframe_order()

    if df.empty:
        st.warning("Belum ada data.")
        return

    df["total"] = df["total"].astype(float)
    df["tanggal_order"] = pd.to_datetime(df["tanggal_order"])

    st.subheader("📅 Filter Tanggal")

    min_date = df["tanggal_order"].min().date()
    max_date = df["tanggal_order"].max().date()

    # Fitur filter: bisa single, bisa rentang tanggal
    date_range = st.date_input(
        "Pilih tanggal (bisa satu atau rentang):",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Penyesuaian agar support single-date & multi-date
    if isinstance(date_range, list) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, list) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    elif isinstance(date_range, (tuple, set)) and len(date_range) == 2:
        start_date, end_date = list(date_range)
    elif isinstance(date_range, (datetime, pd.Timestamp)):
        start_date = end_date = date_range
    else:
        st.warning("Pilih tanggal yang valid.")
        return

    df_filtered = df[
        (df["tanggal_order"].dt.date >= start_date) &
        (df["tanggal_order"].dt.date <= end_date)
    ]

    if df_filtered.empty:
        st.warning("Tidak ada data pada rentang tanggal ini.")
        return

    total = df_filtered["total"].sum()
    st.metric(label="💰 Total Pendapatan",
              value=f"Rp {total:,.0f}".replace(",", "."))

    st.subheader("📊 Grafik Pendapatan per Jenis Transaksi")
    pendapatan_per_jenis = df_filtered.groupby("jenis_transaksi")["total"].sum().sort_values(ascending=False)
    st.bar_chart(pendapatan_per_jenis)

    st.subheader("📋 Riwayat Order")

    df_display = df_filtered.copy()
    df_display["total"] = df_display["total"].apply(
        lambda x: f"Rp {int(x):,}".replace(",", "."))
    df_display["tanggal_order"] = df_display["tanggal_order"].dt.strftime("%d-%m-%Y")

    df_display = df_display.rename(columns={
        "id_order": "ID",
        "nama_pelanggan": "Nama",
        "status_pelanggan": "Status",
        "list_barang": "Barang",
        "jenis_transaksi": "Jenis",
        "jumlah": "Jumlah",
        "metode_pembayaran": "Pembayaran",
        "tanggal_order": "Tanggal",
        "total": "Total"
    }).set_index("ID")

    st.markdown("""
        <style>
        .row-heading.level0, .blank {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.dataframe(df_display, use_container_width=True)

    with st.expander("📥 Download Data"):
        st.download_button(
            label="Download sebagai CSV",
            data=df_display.reset_index().to_csv(index=False),
            file_name="riwayat_inventaris.csv",
            mime="text/csv"
        )

main()

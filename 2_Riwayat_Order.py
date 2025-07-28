import streamlit as st
from admin_auth import AdminAuthenticator
from manajer_order import ManajerOrderInventaris

st.set_page_config(page_title="Riwayat Order Inventaris", page_icon="🗃️")
st.title("🗃️ Riwayat Order (Panel Admin)")

auth = AdminAuthenticator()
auth.login_sidebar()

if auth.is_logged_in():
    manajer = ManajerOrderInventaris()
    df = manajer.get_dataframe_order()

    if df.empty:
        st.info("Belum ada order.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("### Hapus Order")
        id_hapus = st.number_input("ID Order yang ingin dihapus", min_value=1, step=1)
        if st.button("Hapus Order"):
            if manajer.hapus_order(int(id_hapus)):
                st.success("Order berhasil dihapus.")
                st.experimental_rerun()
            else:
                st.error("Gagal hapus order atau ID tidak ditemukan.")
else:
    st.warning("Silakan login sebagai admin untuk mengakses riwayat order.")

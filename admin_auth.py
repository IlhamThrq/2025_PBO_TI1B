import streamlit as st
from abc import ABC, abstractmethod

class BaseAuthenticator(ABC):
    @abstractmethod
    def login_sidebar(self, key_prefix: str = "auth"):
        pass

    @abstractmethod
    def is_logged_in(self) -> bool:
        pass

    @abstractmethod
    def get_username(self) -> str | None:
        pass

    @abstractmethod
    def logout(self):
        pass

class AdminAuthenticator(BaseAuthenticator):
    def __init__(self):
        self._credentials = st.secrets.get("admin_accounts", {})
        if "is_admin" not in st.session_state:
            st.session_state["is_admin"] = False
        if "admin_username" not in st.session_state:
            st.session_state["admin_username"] = None

    def login_sidebar(self, key_prefix="auth"):
        with st.sidebar:
            st.markdown("### 🔐 Panel Admin")
            if self.is_logged_in():
                st.success(f"✅ Login sebagai: {self.get_username()}")
                if st.button("Logout", key=f"{key_prefix}_logout_btn"):
                    self.logout()
                    st.rerun()
            else:
                username = st.text_input("Username", key=f"{key_prefix}_username")
                password = st.text_input("Password", type="password", key=f"{key_prefix}_password")
                if st.button("Login", key=f"{key_prefix}_login_btn"):
                    if username in self._credentials and password == self._credentials[username]:
                        st.session_state["is_admin"] = True
                        st.session_state["admin_username"] = username
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah.")

    def is_logged_in(self) -> bool:
        return st.session_state.get("is_admin", False)

    def get_username(self) -> str | None:
        return st.session_state.get("admin_username")

    def logout(self):
        st.session_state["is_admin"] = False
        st.session_state["admin_username"] = None

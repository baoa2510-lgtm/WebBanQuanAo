import streamlit as st
from database import init_db, connect, verify_password

st.set_page_config(page_title="Đăng nhập", page_icon="🔐")
init_db()
st.title("🔐 Đăng nhập quản trị")

if st.session_state.get("logged_in", False):
    st.success(f"Đang đăng nhập với tài khoản: {st.session_state.get('username', '')}")
    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Đã đăng xuất.")
        st.rerun()
else:
    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập")

    if submitted:
        with connect() as conn:
            user = conn.execute(
                "SELECT password_hash FROM users WHERE username=?",
                (username.strip(),)
            ).fetchone()
        if user and verify_password(password, user["password_hash"]):
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.success("Đăng nhập thành công.")
            st.rerun()
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không đúng.")

st.caption("Tài khoản demo: admin / admin123. Đổi mật khẩu trước khi dùng thật.")

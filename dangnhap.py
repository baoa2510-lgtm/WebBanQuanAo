
import streamlit as st
from database import connect, hash_password, check_password

st.title("Tài khoản")

action = st.radio("Chọn chức năng", ["Đăng nhập", "Đăng ký"])

username = st.text_input("Tên đăng nhập")
password = st.text_input("Mật khẩu", type="password")

if st.button(action):
    if not username.strip() or not password:
        st.error("Vui lòng nhập đầy đủ thông tin.")
    else:
        with connect() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username=?",
                (username.strip(),)
            ).fetchone()

            if action == "Đăng nhập":
                if user and check_password(password, user[1]):
                    st.session_state.logged_in = True
                    st.session_state.username = user[0]
                    st.session_state.role = user[2]
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai tên đăng nhập hoặc mật khẩu.")

            elif user:
                st.error("Tên đăng nhập đã tồn tại.")
            else:
                conn.execute("""
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, 'user')
                """, (username.strip(), hash_password(password)))

                st.success("Đăng ký thành công! Hãy đăng nhập.")

if st.session_state.get("logged_in", False):
    st.write("Đang đăng nhập:", st.session_state.username)

    if st.button("Đăng xuất"):
        st.session_state.clear()
        st.rerun()

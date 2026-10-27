
import streamlit as st
from database import init_db

st.set_page_config(
    page_title="Đăng nhập - Shop quần áo",
    page_icon="👕",
    layout="centered"
)

init_db()

# Kiểm tra trạng thái đăng nhập
if not st.session_state.get("logged_in", False):
    st.title("👕 SHOP QUẦN ÁO")
    st.subheader("Đăng nhập để tiếp tục")

    # Giữ trang đăng nhập riêng biệt
    st.page_link(
        "pages/5_DangNhap.py",
        label="🔐 Đăng nhập / Đăng ký",
        use_container_width=True
    )

    st.info("Vui lòng nhấn nút trên để đăng nhập hoặc đăng ký.")

else:
    st.title("👕 SHOP QUẦN ÁO")
    st.success(
        f"Xin chào, {st.session_state.get('username', 'người dùng')}!"
    )

    st.write("Bạn đã đăng nhập thành công.")

    if st.button("Đăng xuất"):
        st.session_state.clear()
        st.rerun()

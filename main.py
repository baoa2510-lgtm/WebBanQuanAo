
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Shop quần áo",
    page_icon="👕",
    layout="centered"
)

pages_dir = Path(__file__).parent / "pages"

login_page = st.Page(
    str(pages_dir / "DangNhap.py"),
    title="Đăng nhập / Đăng ký",
    icon="🔐",
    default=True
)

admin_page = st.Page(
    str(pages_dir / "Admin.py"),
    title="Admin",
    icon="⚙️"
)

add_page = st.Page(
    str(pages_dir / "Them.py"),
    title="Thêm sản phẩm",
    icon="➕"
)

edit_page = st.Page(
    str(pages_dir / "Sua.py"),
    title="Sửa sản phẩm",
    icon="✏️"
)

delete_page = st.Page(
    str(pages_dir / "Xoa.py"),
    title="Xóa sản phẩm",
    icon="🗑️"
)

navigation = st.navigation([
    login_page,
    admin_page,
    add_page,
    edit_page,
    delete_page
])

navigation.run()

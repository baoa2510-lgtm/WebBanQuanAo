import streamlit as st
from database import init_db, connect, require_login

st.set_page_config(page_title="Thêm sản phẩm", page_icon="➕")
init_db()
st.title("➕ Thêm sản phẩm")
require_login()

with st.form("add_product", clear_on_submit=True):
    name = st.text_input("Tên sản phẩm *")
    category = st.selectbox("Danh mục", ["Áo", "Quần", "Áo khoác", "Phụ kiện", "Khác"])
    price = st.number_input("Giá (VNĐ)", min_value=0, value=99000, step=1000)
    stock = st.number_input("Số lượng tồn kho", min_value=0, value=1, step=1)
    description = st.text_area("Mô tả")
    image_url = st.text_input("Link ảnh (không bắt buộc)")
    submitted = st.form_submit_button("Thêm sản phẩm")

if submitted:
    if not name.strip():
        st.error("Vui lòng nhập tên sản phẩm.")
    else:
        with connect() as conn:
            conn.execute("""
                INSERT INTO products (name, category, price, stock, description, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name.strip(), category, int(price), int(stock), description.strip(), image_url.strip()))
        st.success(f"Đã thêm sản phẩm: {name.strip()}")

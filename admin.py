
import streamlit as st
from database import get_products, money, require_admin

st.title("Quản lý sản phẩm")
require_admin()

products = get_products()

for p in products:
    st.write("Mã:", p["id"])
    st.write("Tên:", p["name"])
    st.write("Danh mục:", p["category"])
    st.write("Giá:", money(p["price"]))
    st.write("Số lượng:", p["stock"])
    st.divider()

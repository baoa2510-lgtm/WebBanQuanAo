
import streamlit as st
from database import connect, get_products, require_admin

st.title("Xóa sản phẩm")
require_admin()

products = get_products()

if products:
    names = {
        f'{p["id"]} - {p["name"]}': p["id"]
        for p in products
    }

    selected = st.selectbox("Chọn sản phẩm", list(names.keys()))

    if st.button("Xóa sản phẩm"):
        with connect() as conn:
            conn.execute(
                "DELETE FROM products WHERE id=?",
                (names[selected],)
            )

        st.success("Đã xóa sản phẩm!")
        st.rerun()
else:
    st.info("Không có sản phẩm để xóa.")

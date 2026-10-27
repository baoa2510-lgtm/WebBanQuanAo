import streamlit as st
from database import init_db, connect, get_products, money, require_login

st.set_page_config(page_title="Xóa sản phẩm", page_icon="🗑️")
init_db()
st.title("🗑️ Xóa sản phẩm")
require_login()

products = get_products()
if not products:
    st.info("Không có sản phẩm để xóa.")
    st.stop()

options = {f"#{p['id']} — {p['name']} ({money(p['price'])})": p for p in products}
choice = st.selectbox("Chọn sản phẩm cần xóa", list(options.keys()))
selected = options[choice]
st.warning(f"Bạn đang chọn: **{selected['name']}**. Thao tác xóa không thể tự hoàn tác.")
confirm = st.checkbox("Tôi xác nhận muốn xóa sản phẩm này.")

if st.button("Xóa sản phẩm", type="primary", disabled=not confirm):
    with connect() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (selected["id"],))
    st.success("Đã xóa sản phẩm.")
    st.rerun()

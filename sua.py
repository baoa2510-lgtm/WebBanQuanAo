import streamlit as st
from database import init_db, connect, get_products, require_login

st.set_page_config(page_title="Sửa sản phẩm", page_icon="✏️")
init_db()
st.title("✏️ Sửa sản phẩm")
require_login()

products = get_products()
if not products:
    st.info("Chưa có sản phẩm.")
    st.stop()

options = {f"#{p['id']} — {p['name']}": p for p in products}
choice = st.selectbox("Chọn sản phẩm cần sửa", list(options.keys()))
p = options[choice]
categories = ["Áo", "Quần", "Áo khoác", "Phụ kiện", "Khác"]
cat = p["category"] if p["category"] in categories else "Khác"

with st.form("edit_product"):
    name = st.text_input("Tên sản phẩm", value=p["name"])
    category = st.selectbox("Danh mục", categories, index=categories.index(cat))
    price = st.number_input("Giá (VNĐ)", min_value=0, value=int(p["price"]), step=1000)
    stock = st.number_input("Số lượng tồn kho", min_value=0, value=int(p["stock"]), step=1)
    description = st.text_area("Mô tả", value=p["description"] or "")
    image_url = st.text_input("Link ảnh", value=p["image_url"] or "")
    submitted = st.form_submit_button("Lưu thay đổi")

if submitted:
    if not name.strip():
        st.error("Tên sản phẩm không được để trống.")
    else:
        with connect() as conn:
            conn.execute("""
                UPDATE products
                SET name=?, category=?, price=?, stock=?, description=?, image_url=?
                WHERE id=?
            """, (name.strip(), category, int(price), int(stock), description.strip(),
                  image_url.strip(), p["id"]))
        st.success("Đã cập nhật sản phẩm.")
        st.rerun()


import streamlit as st
from database import connect, get_products, require_admin

st.title("Sửa sản phẩm")
require_admin()

products = get_products()

if products:
    ids = [p["id"] for p in products]
    selected = st.selectbox("Chọn mã sản phẩm", ids)
    product = next(p for p in products if p["id"] == selected)

    with st.form("sua_san_pham"):
        name = st.text_input("Tên sản phẩm", product["name"])
        category = st.text_input("Danh mục", product["category"])
        price = st.number_input(
            "Giá tiền", min_value=0, value=product["price"]
        )
        stock = st.number_input(
            "Số lượng", min_value=0, value=product["stock"]
        )
        description = st.text_area(
            "Mô tả", product["description"] or ""
        )

        submit = st.form_submit_button("Lưu thay đổi")

        if submit:
            if name.strip() and price > 0:
                with connect() as conn:
                    conn.execute("""
                        UPDATE products
                        SET name=?, category=?, price=?, stock=?,
                            description=?
                        WHERE id=?
                    """, (
                        name, category, price, stock,
                        description, selected
                    ))

                st.success("Đã cập nhật sản phẩm!")
            else:
                st.error("Tên không được để trống và giá phải lớn hơn 0.")
else:
    st.info("Chưa có sản phẩm.")

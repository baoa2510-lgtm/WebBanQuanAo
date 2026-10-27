
import streamlit as st
import os
from database import connect, require_admin

st.title("Thêm sản phẩm")
require_admin()

name = st.text_input("Tên sản phẩm")
category = st.selectbox("Danh mục", ["Áo", "Quần", "Phụ kiện"])
price = st.number_input("Giá tiền", min_value=1000, step=1000)
stock = st.number_input("Số lượng", min_value=0, step=1)
description = st.text_area("Mô tả")

image = st.file_uploader(
    "Chọn ảnh sản phẩm",
    type=["jpg", "jpeg", "png", "webp"],
    key="anh_san_pham"
)

if st.button("Thêm sản phẩm"):
    if not name.strip():
        st.error("Vui lòng nhập tên sản phẩm!")

    else:
        image_url = ""

        # Lưu ảnh nếu người dùng đã chọn ảnh
        if image is not None:
            os.makedirs("images", exist_ok=True)

            image_url = os.path.abspath(
                os.path.join("images", image.name)
            )

            with open(image_url, "wb") as f:
                f.write(image.getbuffer())

        # Lưu thông tin sản phẩm vào database
        try:
            with connect() as conn:
                conn.execute("""
                    INSERT INTO products
                    (name, category, price, stock, description, image_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    name.strip(),
                    category,
                    price,
                    stock,
                    description,
                    image_url
                ))

            st.success("Thêm sản phẩm thành công!")

            if image_url:
                st.image(image_url, caption=name, width=250)

        except Exception as e:
            st.error(f"Lỗi khi thêm sản phẩm: {e}")

import streamlit as st
from database import init_db, get_products, money

st.set_page_config(page_title="Shop Quần Áo Basic", page_icon="👕", layout="wide")
init_db()

st.title("👕 Shop Quần Áo Basic")
st.write("Chào mừng bạn đến với cửa hàng quần áo.")

products = get_products()
if not products:
    st.info("Cửa hàng chưa có sản phẩm.")
else:
    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            with st.container(border=True):
                if p["image_url"]:
                    st.image(p["image_url"], use_container_width=True)
                else:
                    st.markdown("# 👕")
                st.subheader(p["name"])
                st.caption(f"Danh mục: {p['category']}")
                st.markdown(f"### {money(p['price'])}")
                st.write(f"Tồn kho: {p['stock']}")
                if p["description"]:
                    st.write(p["description"])

st.sidebar.info("Chọn trang ở thanh bên. Đăng nhập để vào khu vực quản trị.")

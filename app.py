import streamlit as st
import os

# Cấu hình trang
st.set_page_config(page_title="Cửa Hàng Thời Trang", layout="wide")

# Tạo thư mục uploads nếu chưa có
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- KHỞI TẠO DỮ LIỆU ---
if "users" not in st.session_state:
    st.session_state.users = {"admin": "123", "khachhang": "123"}

if "products" not in st.session_state:
    st.session_state.products = [
        {
            "id": 1,
            "name": "Áo Thun Basic Trắng",
            "price": 150000,
            "size": "M, L, XL",
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
        },
        {
            "id": 2,
            "name": "Quần Jeans Xanh Classic",
            "price": 350000,
            "size": "29, 30, 31, 32",
            "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"
        }
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- THANH BÊN (ĐĂNG NHẬP / ĐĂNG KÝ & ĐIỀU HƯỚNG) ---
with st.sidebar:
    st.title("Menu")
    menu = st.radio("Chọn trang:", ["🏠 Trang Chủ", "🛍️ Cửa Hàng"])
    
    st.divider()
    st.title("Tài Khoản")
    
    if not st.session_state.logged_in:
        tab_login, tab_register = st.tabs(["Đăng nhập", "Tạo tài khoản"])
        
        with tab_login:
            u_login = st.text_input("Tên đăng nhập", key="login_user")
            p_login = st.text_input("Mật khẩu", type="password", key="login_pass")
            if st.button("Đăng nhập", use_container_width=True):
                if u_login in st.session_state.users and st.session_state.users[u_login] == p_login:
                    st.session_state.logged_in = True
                    st.session_state.username = u_login
                    st.rerun()
                else:
                    st.error("Sai tên đăng nhập hoặc mật khẩu!")
                    
        with tab_register:
            u_reg = st.text_input("Tên đăng nhập mới", key="reg_user")
            p_reg = st.text_input("Mật khẩu mới", type="password", key="reg_pass")
            if st.button("Đăng ký", use_container_width=True):
                if not u_reg or not p_reg:
                    st.warning("Vui lòng nhập đầy đủ thông tin.")
                elif u_reg in st.session_state.users:
                    st.error("Tài khoản đã tồn tại!")
                else:
                    st.session_state.users[u_reg] = p_reg
                    st.success("Tạo tài khoản thành công! Hãy sang tab Đăng nhập.")
    else:
        st.success(f"Xin chào, **{st.session_state.username}**!")
        if st.session_state.username == "admin":
            st.info("⭐ Quản trị viên ")
        else:
            st.info("👤 Khách hàng")
            
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# --- NỘI DUNG TRANG CHỦ ---
if menu == "🏠 Trang Chủ":
    st.title("🌟 Chào Mừng Đến Với Cửa Hàng Thời Trang Đẳng Cấp")
    st.markdown("Nơi cung cấp  thời trang trẻ trung, phong cách.")
    
    st.image("https://report.adidas-group.com/2022/en/_assets/gallery/mag-2-hero.jpg", use_container_width=True)
    
    st.subheader("📊 Tổng Quan Cửa Hàng")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng số sản phẩm", len(st.session_state.products))
    col_m2.metric("Thành viên hệ thống", len(st.session_state.users))
    col_m3.metric("Trạng thái", "Đang hoạt động 🟢")
    
    st.divider()
    st.markdown("👉 Hãy chọn mục **🛍️ Trang chủ** ở thanh menu bên trái để xem chi tiết các sản phẩm hoặc đăng nhập quản trị.")

# --- NỘI DUNG TRANG CỬA HÀNG & QUẢN LÝ ---
elif menu == "🛍️ Trang chủ":
    st.title("👕 Cửa Hàng Quần Áo Trực Tuyến")

    is_admin = st.session_state.logged_in and (st.session_state.username == "admin")

    if is_admin:
        st.success("🔓 Chào Admin!")
        with st.expander("➕ Thêm sản phẩm mới"):
            with st.form("add_form", clear_on_submit=True):
                col_f1, col_f2 = st.columns(2)
                new_name = col_f1.text_input("Tên sản phẩm")
                new_price = col_f2.number_input("Giá bán (VNĐ)", min_value=0, step=10000)
                new_size = col_f1.text_input("Kích cỡ (VD: S, M, L)")
                
                uploaded_file = st.file_uploader("Tải ảnh sản phẩm từ máy tính", type=["jpg", "jpeg", "png"])
                
                if st.form_submit_button("Lưu sản phẩm"):
                    if new_name:
                        image_path = "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
                        
                        if uploaded_file is not None:
                            image_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                            with open(image_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                        
                        new_id = max([p["id"] for p in st.session_state.products], default=0) + 1
                        st.session_state.products.append({
                            "id": new_id,
                            "name": new_name,
                            "price": new_price,
                            "size": new_size,
                            "image": image_path
                        })
                        st.success("Đã thêm sản phẩm kèm ảnh thành công!")
                        st.rerun()
                    else:
                        st.warning("Tên sản phẩm không được để trống.")
    st.divider()

    st.subheader("Danh sách sản phẩm")

    if not st.session_state.products:
        st.write("Hiện chưa có sản phẩm nào.")
    else:
        cols = st.columns(3)
        for index, item in enumerate(st.session_state.products):
            with cols[index % 3]:
                with st.container(border=True):
                    st.image(item["image"], use_container_width=True)
                    st.markdown(f"### {item['name']}")
                    st.write(f"**Giá:** {item['price']:,} VNĐ")
                    st.write(f"**Size:** {item['size']}")
                    
                    if is_admin:
                        c1, c2 = st.columns(2)
                        
                        if c1.button("🗑️ Xóa", key=f"del_{item['id']}", use_container_width=True):
                            st.session_state.products = [p for p in st.session_state.products if p["id"] != item["id"]]
                            st.rerun()
                            
                        with c2.popover("✏️ Sửa", use_container_width=True):
                            edit_name = st.text_input("Tên", value=item["name"], key=f"ename_{item['id']}")
                            edit_price = st.number_input("Giá", value=item["price"], step=10000, key=f"eprice_{item['id']}")
                            edit_size = st.text_input("Size", value=item["size"], key=f"esize_{item['id']}")
                            
                            edit_file = st.file_uploader("Thay đổi ảnh từ máy", type=["jpg", "jpeg", "png"], key=f"efile_{item['id']}")
                            
                            if st.button("Cập nhật", key=f"save_{item['id']}"):
                                item["name"] = edit_name
                                item["price"] = edit_price
                                item["size"] = edit_size
                                
                                if edit_file is not None:
                                    edit_image_path = os.path.join(UPLOAD_DIR, edit_file.name)
                                    with open(edit_image_path, "wb") as f:
                                        f.write(edit_file.getbuffer())
                                    item["image"] = edit_image_path
                                    
                                st.rerun()

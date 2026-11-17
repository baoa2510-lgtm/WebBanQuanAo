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
    st.title("📂 Menu Điều Hướng")
    # Tạo menu chuyển đổi giữa Trang chủ và Cửa hàng sản phẩm
    menu = st.radio("Chọn trang:", ["🏠 Trang Chủ", "🛍️ Cửa Hàng & Quản Lý"])
    
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
            st.info("⭐ Quyền hạn: Quản trị viên (Admin)")
        else:
            st.info("👤 Quyền hạn: Khách hàng")
            
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# --- NỘI DUNG TRANG CHỦ ---
if menu == "🏠 Trang Chủ":
    st.title("🌟 Chào Mừng Đến Với Cửa Hàng Thời Trang")
    st.markdown("Nơi cung cấp các xu hướng thời trang trẻ trung, năng động và phong cách.")
    
    # Banner / Hình ảnh giới thiệu trang chủ
    st.image("https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200", use_container_width=True)
    
    st.subheader("📊 Tổng Quan Cửa Hàng")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sản phẩm", len(st.session_state.products))
    col2.metric("Thành viên hệ thống", len(st.session_state.users))
    col3.metric("Trạng thái", "Đang hoạt động 🟢")
    
    st.divider()
    st.markdown("👉 Hãy chọn mục **🛍️ Cửa Hàng & Quản Lý** ở thanh menu bên trái để xem chi tiết các sản phẩm hoặc đăng nhập quản trị.")

# --- NỘI DUNG TRANG CỬA HÀNG & QUẢN LÝ ---
elif menu == "🛍️ Cửa Hàng & Quản Lý":
    st.title("👕 Cửa Hàng Quần Áo Trực Tuyến")

    # Kiểm tra nếu là ADMIN thì mới hiện form Thêm sản phẩm
    is_admin = st.session_state.logged_in and (st.session_state.username == "admin")

    if is_admin:
        st.success("🔓 Chào Admin! Bạn có quyền Thêm, Sửa, Xóa sản phẩm.")
        with st.expander("➕ Thêm sản phẩm mới"):
            with st.form("add_form", clear_on_submit=True):
                col1, col2

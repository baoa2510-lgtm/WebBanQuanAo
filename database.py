import sqlite3
import hashlib
import hmac
import os
from pathlib import Path

DB_PATH = Path(__file__).with_name("shop.db")

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt=None):
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex() + ":" + digest.hex()

def verify_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split(":")
        candidate = hash_password(password, bytes.fromhex(salt_hex)).split(":")[1]
        return hmac.compare_digest(candidate, digest_hex)
    except (ValueError, TypeError):
        return False

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                description TEXT DEFAULT '',
                image_url TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """)
        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            conn.executemany("""
                INSERT INTO products (name, category, price, stock, description, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                ("Áo thun basic", "Áo", 99000, 20, "Áo thun cotton mặc hằng ngày.", ""),
                ("Áo sơ mi trắng", "Áo", 189000, 12, "Sơ mi đơn giản, dễ phối đồ.", ""),
                ("Quần jeans xanh", "Quần", 259000, 8, "Quần jeans dáng cơ bản.", ""),
            ])
        if not conn.execute("SELECT 1 FROM users WHERE username = ?", ("admin",)).fetchone():
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                         ("admin", hash_password("admin123")))

def get_products(search=""):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM products WHERE name LIKE ? ORDER BY id DESC",
            (f"%{search}%",)
        ).fetchall()

def money(value):
    return f"{int(value):,} đ".replace(",", ".")

def require_login():
    import streamlit as st
    if not st.session_state.get("logged_in", False):
        st.warning("Bạn cần đăng nhập trước khi sử dụng chức năng quản trị.")
        st.info("Mở trang **5_ĐangNhap** ở thanh bên để đăng nhập.")
        st.stop()

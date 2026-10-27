
import sqlite3
import hashlib
import os
import hmac
from pathlib import Path

DB_PATH = Path(__file__).with_name("shop.db")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 100000
    )
    return salt.hex() + ":" + hashed.hex()


def check_password(password, saved_password):
    try:
        salt, old_hash = saved_password.split(":")
        new_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(),
            bytes.fromhex(salt), 100000
        ).hex()
        return hmac.compare_digest(new_hash, old_hash)
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
                stock INTEGER DEFAULT 0,
                description TEXT DEFAULT '',
                image_url TEXT DEFAULT ''
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)

        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            conn.executemany("""
                INSERT INTO products
                (name, category, price, stock, description)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("Áo thun", "Áo", 99000, 20, "Áo thun basic"),
                ("Áo sơ mi", "Áo", 189000, 12, "Áo sơ mi trắng"),
                ("Quần jeans", "Quần", 259000, 8, "Quần jeans xanh")
            ])

        admin = conn.execute(
            "SELECT username FROM users WHERE username = ?",
            ("admin",)
        ).fetchone()

        if not admin:
            conn.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, ("admin", hash_password("admin123"), "admin"))

        # Them cot role neu database cu chua co
        columns = [
            row["name"] for row in
            conn.execute("PRAGMA table_info(users)").fetchall()
        ]

        if "role" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'"
            )
            conn.execute(
                "UPDATE users SET role = 'admin' WHERE username = 'admin'"
            )


def get_products(search=""):
    with connect() as conn:
        return conn.execute("""
            SELECT * FROM products
            WHERE name LIKE ?
            ORDER BY id DESC
        """, ("%" + search + "%",)).fetchall()


def money(price):
    return f"{int(price):,} đ".replace(",", ".")


def require_login():
    import streamlit as st

    if not st.session_state.get("logged_in", False):
        st.warning("Vui lòng đăng nhập trước!")
        st.stop()


def require_admin():
    import streamlit as st

    if not st.session_state.get("logged_in", False):
        st.warning("Vui lòng đăng nhập trước!")
        st.stop()

    if st.session_state.get("role") != "admin":
        st.error("Bạn không có quyền quản trị!")
        st.stop()
        
def reset_admin():
    with connect() as conn:
        password = hash_password("admin123")

        user = conn.execute(
            "SELECT username FROM users WHERE username = ?",
            ("admin",)
        ).fetchone()

        if user:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (password, "admin")
            )
        else:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (?, ?, ?)",
                ("admin", password, "admin")
            )

        conn.execute(
            "UPDATE users SET role = 'admin' WHERE username = 'admin'"
        )

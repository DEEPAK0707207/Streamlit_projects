import streamlit as st
import psycopg2
from psycopg2 import IntegrityError


def get_connection():
    return psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
    finally:
        conn.close()


def create_user(username, email, password_hash):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, username, email, role;
            """, (username, email, password_hash))
            user = cur.fetchone()
        conn.commit()
        return user
    except IntegrityError:
        conn.rollback()
        return None
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, password_hash, role
                FROM users
                WHERE username = %s;
            """, (username,))
            return cur.fetchone()
    finally:
        conn.close()
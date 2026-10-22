
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """Connect to the Neon PostgreSQL database."""
    return psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )


def init_db():
    """Create the users table if it does not exist."""
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
    """Register a new user."""
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users
                    (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (username, email, password_hash, "user"),
            )

            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

    finally:
        conn.close()


def get_user_by_username(username):
    """Find one user by username."""
    conn = get_connection()

    try:
        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:
            cur.execute(
                """
                SELECT id, username, email,
                       password_hash, role
                FROM users
                WHERE username = %s;
                """,
                (username,),
            )

            result = cur.fetchone()
            return dict(result) if result else None

    finally:
        conn.close()


def get_all_users():
    """Get users for the admin panel."""
    conn = get_connection()

    try:
        with conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:
            cur.execute("""
                SELECT id, username, email,
                       role, created_at
                FROM users
                ORDER BY id;
            """)

            return [dict(row) for row in cur.fetchall()]

    finally:
        conn.close()


import streamlit as st
from db import init_db, create_user, get_user_by_username
from auth import (
    hash_password,
    verify_password,
    validate_username,
    validate_email,
    validate_password,
)

st.set_page_config(
    page_title="Lab 13 - Authentication",
    page_icon="🔐",
    layout="centered",
)

st.title("🔐 Lab 13: Login and Signup")
st.caption("PostgreSQL Authentication System")

# Initialize the database
try:
    init_db()
except Exception:
    st.error(
        "Cannot connect to the database. "
        "Check your Neon connection and secrets."
    )
    st.stop()

# Logged-in page
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    user = st.session_state.user

    st.success(f"Welcome, {user['username']}!")
    st.write(f"Email: {user['email']}")
    st.write(f"Role: {user['role']}")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

else:
    login_tab, signup_tab = st.tabs(["Login", "Signup"])

    with signup_tab:
        st.subheader("Create an account")

        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input(
                "Password", type="password"
            )
            confirm_password = st.text_input(
                "Confirm password", type="password"
            )
            signup_button = st.form_submit_button(
                "Create Account"
            )

        if signup_button:
            username = new_username.strip()
            email = new_email.strip().lower()

            if not validate_username(username):
                st.error(
                    "Username must be 3–50 characters: "
                    "letters, numbers, or underscores."
                )
            elif not validate_email(email):
                st.error("Enter a valid email address.")
            elif not validate_password(new_password):
                st.error(
                    "Password must contain at least 8 characters."
                )
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                password_hash = hash_password(new_password)

                try:
                    user = create_user(
                        username, email, password_hash
                    )
                    if user:
                        st.success(
                            "Account created! Go to the Login tab."
                        )
                    else:
                        st.error(
                            "Username or email already exists."
                        )
                except Exception:
                    st.error(
                        "Registration failed. Please try again."
                    )

    with login_tab:
        st.subheader("Login to your account")

        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input(
                "Password", type="password", key="login_password"
            )
            login_button = st.form_submit_button("Login")

        if login_button:
            try:
                user = get_user_by_username(username.strip())

                if user and verify_password(password, user[3]):
                    st.session_state.user = {
                        "id": user[0],
                        "username": user[1],
                        "email": user[2],
                        "role": user[4],
                    }
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

            except Exception:
                st.error("Login failed. Please try again.")


import re
import bcrypt

from db import create_user, get_user_by_username


def hash_password(password):
    """Securely hash a password."""
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, stored_hash):
    """Check a password against its stored hash."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def valid_email(email):
    """Basic email format validation."""
    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        )
    )


def register_user(username, email, password):
    """Validate details and register a user."""
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return False, "Username must have at least 3 characters."

    if not valid_email(email):
        return False, "Enter a valid email address."

    if len(password) < 8:
        return False, "Password must have at least 8 characters."

    if get_user_by_username(username):
        return False, "Username already exists."

    try:
        create_user(
            username,
            email,
            hash_password(password)
        )
        return True, "Registration successful!"

    except Exception:
        return False, (
            "Registration failed. The username or email "
            "may already be registered."
        )


def login_user(username, password):
    """Verify login credentials."""
    user = get_user_by_username(username.strip())

    if not user:
        return None

    if verify_password(password, user["password_hash"]):
        return user

    return None

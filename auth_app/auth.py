import re
import bcrypt


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )
    return hashed.decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def validate_username(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,50}", username))


def validate_email(email):
    return bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
    )


def validate_password(password):
    return len(password) >= 8
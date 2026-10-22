print("Starting database test...")

from db import init_db

try:
    init_db()
    print("SUCCESS: Neon connected and users table created!")
except Exception as e:
    print("Database error:")
    print(type(e).__name__, str(e))
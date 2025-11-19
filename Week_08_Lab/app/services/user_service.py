import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role="user"):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    insert_user(username, password_hash, role)
    return True

def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    stored_hash = user[2]  # password_hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Welcome, {username}!"
    return False, "Invalid password."

def migrate_users_from_file(filepath="DATA/users.txt"):
    if not Path(filepath).exists():
        print("No users.txt found. Skipping migration.")
        return 0

    conn = connect_database()
    create_users_table(conn)
    count = 0
    with open(filepath, "r") as f:
        for line in f:
            if line.strip():
                username, hashed_pw = line.strip().split(",", 1)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed_pw)
                )
                if cursor.rowcount > 0:
                    count += 1
    conn.commit()
    conn.close()
    print(f"Migrated {count} users from users.txt")
    return count
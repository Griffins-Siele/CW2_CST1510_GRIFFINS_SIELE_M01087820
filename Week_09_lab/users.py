from pathlib import Path
from typing import Dict
import bcrypt


def _users_file() -> Path:
    return Path(__file__).parent / "users.txt"


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def load_users() -> Dict[str, str]:
    """Load users from users.txt. Returns a dict username->hashed_password.

    File format: one user per line as `username:bcrypt_hash`.
    """
    p = _users_file()
    users = {}
    if not p.exists():
        return users
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                user, pw_hash = line.split(":", 1)
                users[user] = pw_hash
    return users


def save_users(users: Dict[str, str]) -> None:
    """Write the full users dict to users.txt atomically."""
    p = _users_file()
    tmp = p.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for u, pw_hash in users.items():
            f.write(f"{u}:{pw_hash}\n")
    tmp.replace(p)


def add_user(username: str, password: str) -> None:
    """Add a new user with a plaintext password (hashed before storage)."""
    users = load_users()
    users[username] = hash_password(password)
    save_users(users)


def authenticate(username: str, password: str) -> bool:
    """Verify username and password. Returns True if credentials are valid."""
    users = load_users()
    if username not in users:
        return False
    return verify_password(password, users[username])

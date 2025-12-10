"""Authentication module (Week 7).

This module provides secure user authentication using bcrypt hashing.
References Week 7 authentication patterns.
"""

import bcrypt
import os
import re
from pathlib import Path

USER_DATA_FILE = "project/users.txt"


def hash_password(plain_text_password: str) -> str:
    """Hash a password using bcrypt with automatic salt generation.
    
    Args:
        plain_text_password: The plaintext password to hash
        
    Returns:
        The bcrypt hash as a string
    """
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.
    
    Args:
        plain_text_password: The plaintext password to verify
        hashed_password: The stored hash to verify against
        
    Returns:
        True if password matches, False otherwise
        
    Raises:
        ValueError: If passwords are invalid
    """
    if not isinstance(plain_text_password, str) or not plain_text_password:
        raise ValueError("Password must be a non-empty string")
    if not isinstance(hashed_password, str) or not hashed_password:
        raise ValueError("Hash must be a non-empty string")
    
    try:
        password_bytes = plain_text_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        raise ValueError(f"Error verifying password: {e}")


def user_exists(username: str) -> bool:
    """Check if a user already exists.
    
    Args:
        username: The username to check
        
    Returns:
        True if user exists, False otherwise
    """
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                if line.strip():
                    stored_username = line.strip().split(",")[0]
                    if stored_username == username:
                        return True
    except Exception as e:
        print(f"Error checking user existence: {e}")
    
    return False


def register_user(username: str, password: str) -> tuple[bool, str]:
    """Register a new user with secure password hashing.
    
    Args:
        username: The username to register
        password: The plaintext password
        
    Returns:
        Tuple of (success, message)
        
    Raises:
        ValueError: If username or password are invalid
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string")
    if not isinstance(password, str) or len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    if user_exists(username):
        return False, f"Username '{username}' already exists"
    
    try:
        # Ensure directory exists
        Path(USER_DATA_FILE).parent.mkdir(parents=True, exist_ok=True)
        
        hashed_password = hash_password(password)
        with open(USER_DATA_FILE, "a") as file:
            file.write(f"{username},{hashed_password}\n")
        
        return True, f"User '{username}' registered successfully!"
    except Exception as e:
        return False, f"Registration error: {e}"


def login_user(username: str, password: str) -> tuple[bool, str]:
    """Authenticate a user by verifying username and password.
    
    Args:
        username: The username to authenticate
        password: The plaintext password
        
    Returns:
        Tuple of (success, message)
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string")
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")
    
    if not os.path.exists(USER_DATA_FILE):
        return False, "No users registered yet"
    
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(",", 1)
                    if len(parts) == 2:
                        stored_username, stored_hash = parts
                        if stored_username == username:
                            if verify_password(password, stored_hash):
                                return True, f"Login successful for {username}!"
                            else:
                                return False, "Invalid password"
        
        return False, f"User '{username}' not found"
    except ValueError as e:
        return False, f"Authentication error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

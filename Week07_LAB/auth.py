import bcrypt
import os
import re

# Constants
USER_DATA_FILE = "users.txt"

# Core Security Functions 
def hash_password(plain_text_password: str) -> str:
    """Hashes a password using bcrypt with automatic salt generation."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# User Management Functions 

def user_exists(username: str) -> bool:
    """Checks if a username already exists in the user database."""
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if line.strip():
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    return True
    return False

def register_user(username: str, password: str) -> bool:
    """Registers a new user by hashing their password and storing credentials."""
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_password}\n")
    
    print(f"Success: User '{username}' registered successfully!")
    return True

def login_user(username: str, password: str) -> bool:
    """Authenticates a user by verifying their username and password."""
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if line.strip():
                stored_username, stored_hash = line.strip().split(",", 1)
                if stored_username == username:
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
    print("Error: Username not found.")
    return False

# Input Validation 

def validate_username(username: str):
    """Validates username format: 3-20 alphanumeric characters only."""
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    if not re.match("^[a-zA-Z0-9]+$", username):
        return False, "Username can only contain letters and numbers."
    return True, ""

def validate_password(password: str):
    """Validates password strength: at least 6 characters."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password cannot exceed 50 characters."
    return True, ""

# Interactive Interface 

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

# Temporary test code (remove before final submission if required)
# Uncomment to test hashing functions
"""
test_password = "SecurePassword123"
hashed = hash_password(test_password)
print(f"Hashed: {hashed}")
print(f"Correct password check: {verify_password(test_password, hashed)}")
print(f"Wrong password check: {verify_password('wrong', hashed)}")
"""

if __name__ == "__main__":
    main()
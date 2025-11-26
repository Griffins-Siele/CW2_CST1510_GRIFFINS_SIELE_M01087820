import streamlit as st
import users as users_module
from session_state import init_session

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# Initialize session_state keys used across the app
init_session()

st.title("🔐 Welcome")

# If already logged in, go straight to dashboard (optional)
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
            # Use the official navigation API to switch pages
        st.switch_page("pages/DataManager.py")  # updated target to match pages/Dashboard.py
    st.stop()  # Don’t show login/register again


# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        # Use bcrypt-verified authentication
        if users_module.authenticate(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}! ")

            # Redirect to dashboard page
            st.switch_page("pages/DataManager.py")
        else:
            st.error("Invalid username or password.")


# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        # Basic checks
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            # Use users_module.add_user() which hashes the password before saving
            users_module.add_user(new_username, new_password)
            # Refresh session_state to include the new user
            st.session_state.users = users_module.load_users()
            st.success("Account created! You can now log in from the Login tab.")
            st.info("Passwords are securely hashed with bcrypt before storage.")

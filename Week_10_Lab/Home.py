import streamlit as st
import users as users_module
from session_state import init_session

st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

# Initialize session_state keys used across the app
init_session()

st.title("🔐 Welcome to IT Support Dashboard")

# If already logged in, present a quick navigation option
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to Data Manager"):
        st.switch_page("pages/DataManager.py")
    st.divider()
    st.stop()

# Login / Register tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        if users_module.authenticate(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            users_module.add_user(new_username, new_password)
            st.session_state.users = users_module.load_users()
            st.success("Account created! You can now log in from the Login tab.")
            st.info("Passwords are securely hashed with bcrypt before storage.")

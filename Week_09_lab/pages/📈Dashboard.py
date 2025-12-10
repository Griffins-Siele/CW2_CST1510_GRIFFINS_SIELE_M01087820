import streamlit as st
from session_state import init_session

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

init_session()

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.title("📊 Dashboard")
st.success(f"Welcome, **{st.session_state.username}**! 🎉")

st.divider()

# Quick stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Account Status",
        value="Active",
    )

with col2:
    st.metric(
        label="Pages Available",
        value="5+"
    )

with col3:
    st.metric(
        label="Session Duration",
        value="Active",
    )

st.divider()

st.subheader("Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Data Manager", use_container_width=True):
        st.switch_page("pages/📈Dashboard.py")

with col2:
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/📊Analytics.py")

with col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/⚙️Settings.py")

st.divider()

st.subheader("📌 What can you do?")

st.write("""
- **📋 Data Manager**: Create, read, update, and delete IT support tickets
- **📊 Analytics**: View ticket statistics and visualizations with filters
- **⚙️ Settings**: Manage your profile, preferences, and security settings
""")

st.divider()
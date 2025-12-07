"""Helper to initialize Streamlit session_state keys used across the app.
This file mirrors the implementation used in Week_09_lab so the pages under
`Week_10_Lab/pages` can import `init_session` as expected.
"""
from typing import Dict
import streamlit as st
import users


def init_session() -> None:
    """Ensure all expected session_state keys exist with sensible defaults.

    Keys initialized:
    - users: Dict[str, str] loaded from users.txt
    - logged_in: bool
    - username: str
    - flash: list[str] (optional transient messages)
    """
    if "users" not in st.session_state:
        st.session_state.users = users.load_users()
    else:
        # refresh to reflect any external changes
        st.session_state.users = users.load_users()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "flash" not in st.session_state:
        st.session_state.flash = []

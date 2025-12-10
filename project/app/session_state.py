"""Session state management for Streamlit (Week 9).

References Week 9 Streamlit state management patterns.
"""

import streamlit as st
from typing import Any, Optional


def init_session():
    """Initialize session state keys for the application."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "username" not in st.session_state:
        st.session_state.username = None
    
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    if "selected_dataset" not in st.session_state:
        st.session_state.selected_dataset = None
    
    if "filters" not in st.session_state:
        st.session_state.filters = {}


def logout():
    """Clear session state and logout user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.selected_dataset = None
    st.session_state.filters = {}


def set_value(key: str, value: Any) -> None:
    """Set a session state value.
    
    Args:
        key: State key
        value: Value to set
    """
    st.session_state[key] = value


def get_value(key: str, default: Any = None) -> Any:
    """Get a session state value.
    
    Args:
        key: State key
        default: Default value if key not found
        
    Returns:
        The session value or default
    """
    return st.session_state.get(key, default)


def is_logged_in() -> bool:
    """Check if user is logged in.
    
    Returns:
        True if logged in, False otherwise
    """
    return st.session_state.get("logged_in", False)


def get_current_user() -> Optional[str]:
    """Get the current logged-in username.
    
    Returns:
        Username if logged in, None otherwise
    """
    return st.session_state.get("username") if is_logged_in() else None

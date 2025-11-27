import streamlit as st
from session_state import init_session

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

init_session()

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.title("⚙️ Settings")
st.success(f"Logged in as: **{st.session_state.username}**")

# Create tabs for different settings sections
tab_profile, tab_preferences, tab_security = st.tabs(["👤 Profile", "🎨 Preferences", "🔐 Security"])

# Profile Tab
with tab_profile:
    st.subheader("User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Username:**")
        st.code(st.session_state.username)
        
        st.write("**User ID:**")
        st.code(f"user_{hash(st.session_state.username) % 10000}")
    
    with col2:
        st.write("**Account Status:**")
        st.info("✅ Active")
        
        st.write("**Last Login:**")
        st.caption("Just now")
    
    st.divider()
    
    with st.form("profile_edit_form"):
        st.subheader("Edit Profile Information")
        email = st.text_input("Email", value=f"{st.session_state.username}@example.com")
        full_name = st.text_input("Full Name", value=st.session_state.username.capitalize())
        department = st.selectbox("Department", ["IT", "HR", "Finance", "Operations", "Security"])
        
        if st.form_submit_button("Save Profile"):
            st.success("✅ Profile updated successfully!")


# Preferences Tab
with tab_preferences:
    st.subheader("User Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Theme**")
        theme = st.selectbox("Select Theme:", ["Light", "Dark", "Auto"])
        
        st.write("**Language**")
        language = st.selectbox("Select Language:", ["English", "Spanish", "French", "German"])
    
    with col2:
        st.write("**Notifications**")
        email_notifications = st.checkbox("Email Notifications", value=True)
        alerts = st.checkbox("Security Alerts", value=True)
        updates = st.checkbox("Product Updates", value=False)
    
    st.divider()
    
    st.write("**Data & Privacy**")
    col3, col4 = st.columns(2)
    
    with col3:
        data_retention = st.select_slider(
            "Data Retention (months):",
            options=[3, 6, 12, 24, 36],
            value=12
        )
    
    with col4:
        sharing = st.selectbox("Share Usage Data:", ["Never", "With Support Only", "Anonymous", "Full"])
    
    if st.button("💾 Save Preferences"):
        st.success("✅ Preferences saved successfully!")


# Security Tab
with tab_security:
    st.subheader("Security Settings")
    
    st.write("**Password Management**")
    with st.form("password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if not current_password or not new_password:
                st.error("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            else:
                st.success("✅ Password changed successfully!")
    
    st.divider()
    
    st.write("**Active Sessions**")
    st.info("📍 **Current Session**\n - Device: Windows PC\n - IP: 192.168.1.100\n - Last Active: Just now")
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("You have been logged out.")
        st.switch_page("Home.py")
    
    st.divider()
    
    st.write("**Two-Factor Authentication (2FA)**")
    col_2fa_1, col_2fa_2 = st.columns(2)
    
    with col_2fa_1:
        st.write("Status: ⚠️ **Disabled**")
    
    with col_2fa_2:
        if st.button("🔒 Enable 2FA"):
            st.info("2FA can be enabled via authenticator app (Google Authenticator, Authy, etc.)")
    
    st.divider()
    
    st.write("**Account Actions**")
    if st.button("🗑️ Delete Account", type="secondary"):
        st.warning("⚠️ This action cannot be undone. Your account and all data will be permanently deleted.")
        if st.button("Confirm Deletion", key="confirm_delete"):
            st.error("Account deletion initiated. You will be logged out.")

st.divider()
st.caption("💡 Settings are saved automatically. For security issues, contact support.")

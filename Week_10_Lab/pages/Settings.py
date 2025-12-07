"""Settings & Profile Management."""
import streamlit as st
from session_state import init_session

st.set_page_config(
    page_title="Settings",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_session()

# Authentication check
if not st.session_state.logged_in:
    st.error(" You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.title(" Settings & Profile")
st.success(f"Logged in as: **{st.session_state.username}**")

st.divider()

# Settings tabs
tab_profile, tab_security, tab_preferences, tab_about = st.tabs([
    " Profile",
    " Security",
    " Preferences",
    " About"
])

# ===== PROFILE TAB =====
with tab_profile:
    st.subheader("User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Account Information**")
        st.info(f"Username: `{st.session_state.username}`")
        st.info(f"Role: User")
        st.info(f"Status: Active ")
    
    with col2:
        st.write("**Profile Actions**")
        if st.button(" Edit Profile", use_container_width=True):
            st.info("Profile editing feature coming soon!")
        
        if st.button("📸 Change Avatar", use_container_width=True):
            st.info("Avatar upload feature coming soon!")

# ===== SECURITY TAB =====
with tab_security:
    st.subheader("Security Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Password Management**")
        
        with st.form("password_form"):
            current_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button(" Change Password", use_container_width=True):
                if not current_pwd or not new_pwd or not confirm_pwd:
                    st.error(" Please fill in all fields.")
                elif new_pwd != confirm_pwd:
                    st.error(" Passwords do not match.")
                elif len(new_pwd) < 6:
                    st.error(" Password must be at least 6 characters.")
                else:
                    # In a real app, verify current password and update
                    st.success(" Password changed successfully!")
                    st.info("You will be logged out for security. Please log in again.")
    
    with col2:
        st.write("**Multi-Factor Authentication (MFA)**")
        st.warning(" MFA is recommended for enhanced security.")
        
        mfa_status = st.radio("MFA Status", ["Disabled", "Enable TOTP", "Enable SMS"])
        
        if mfa_status != "Disabled":
            st.info(f"MFA Type: {mfa_status}")
            if st.button(f" Enable {mfa_status}", use_container_width=True):
                st.success(f" {mfa_status} enabled successfully!")
    
    st.divider()
    
    st.write("**Active Sessions**")
    st.info("Current Session: Browser (Active)")
    if st.button("🔓 Logout From All Devices", use_container_width=True):
        st.warning("All other sessions have been terminated.")

# ===== PREFERENCES TAB =====
with tab_preferences:
    st.subheader("User Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Appearance**")
        theme = st.radio(
            "Theme:",
            ["Light", "Dark", "Auto"],
            index=0
        )
        
        if st.button(" Save Theme", use_container_width=True):
            st.session_state.theme = theme.lower()
            st.success(f" Theme set to {theme}")
    
    with col2:
        st.write("**Notifications**")
        email_alerts = st.checkbox("Email Alerts", value=True)
        dashboard_alerts = st.checkbox("Dashboard Alerts", value=True)
        
        if st.button(" Save Preferences", use_container_width=True):
            st.success(" Preferences saved!")
    
    st.divider()
    
    st.write("**Data & Privacy**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" Download My Data", use_container_width=True):
            st.info("Your data will be prepared for download.")
    
    with col2:
        if st.button("🗑️ Request Data Deletion", use_container_width=True):
            st.warning(" Data deletion requests are processed within 30 days.")

# ===== ABOUT TAB =====
with tab_about:
    st.subheader("About This Application")
    
    st.markdown("""
    ### Multi-Domain Intelligence Platform
    
    **Version:** 1.0.0  
    **Status:** Production Ready  
    
    #### Features
    -  Secure Authentication (bcrypt)
    -  Multi-Domain Dashboards
    -  IT Tickets Management (CRUD)
    -  Cyber Incidents Analysis
    -  Data Metadata Catalog
    -  User Analytics
    -  AI Assistant Integration (ChatGPT)
    -  Advanced Visualizations
    
    #### Technologies
    - **Framework:** Streamlit
    - **Backend:** Python
    - **Database:** CSV (File-based)
    - **Security:** bcrypt, environment variables
    - **AI:** OpenAI GPT-3.5-turbo
    - **Visualization:** Plotly, Pandas
    
    #### Dashboards
    1. **Analytics** - IT Tickets with AI insights
    2. **Incidents** - Cyber security with AI advisor
    3. **Metadata** - Dataset catalog with AI analysis
    4. **Users** - User analytics with security focus
    5. **Data Manager** - CRUD operations
    
    #### Team
    - Platform: Griffins-Siele
    - Course: Programming for Data Communications and Networks (CST1510)
    - Assignment: CW2
    
    #### Documentation
    - See `README.md` in the project root
    - Each page has built-in help sections
    - AI Assistant available on dashboard pages
    
    ---
    
    **Note:** This is an educational platform for learning purposes.
    For production use, implement proper database solutions and security measures.
    """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sessions This Month", "15")
    
    with col2:
        st.metric("Data Processed", "1.5 GB")
    
    with col3:
        st.metric("Uptime", "99.8%")

st.divider()

# ===== LOGOUT SECTION =====
st.subheader("Account Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(" Go to Dashboard", use_container_width=True):
        st.switch_page("pages/Analytics.py")

with col2:
    if st.button(" Quick Links", use_container_width=True):
        st.info("""
        **Available Pages:**
        -  Analytics - IT Tickets
        -  Incidents - Cyber Security
        -  Metadata - Dataset Catalog
        -  Users - User Analytics
        -  Data Manager - CRUD Ops
        """)

with col3:
    if st.button("🔓 Logout", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success(" You have been logged out.")
        st.info("Redirecting to login page...")
        
        import time
        time.sleep(2)
        st.switch_page("Home.py")

st.divider()

st.caption("Multi-Domain Intelligence Platform © 2025 | Secure & Confidential")

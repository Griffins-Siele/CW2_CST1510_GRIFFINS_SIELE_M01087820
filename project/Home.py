"""Portfolio Project - Analytics Dashboard

This is a capstone project that integrates learning from Weeks 7-11:
- Week 7: Authentication with bcrypt
- Week 8: Database and data management
- Week 9: Streamlit framework and session state
- Week 10: API integration and data fetching
- Week 11: OOP principles (encapsulation, inheritance, polymorphism)

Application: Data Science Analytics Dashboard
Pathway: Data Science with cyber incident analytics
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.session_state import init_session, is_logged_in, get_current_user

# Configure page
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: ;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session
init_session()

# Title and header
st.title("📊 Data Science Analytics Dashboard")
st.markdown("### Capstone Project - Weeks 7-11 Integration")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    
    if not is_logged_in():
        st.info("👤 Not logged in. Please go to **Home** to login or register.")
    else:
        st.success(f"✅ Logged in as **{get_current_user()}**")
        if st.button("🚪 Logout", type="secondary"):
            from app.session_state import logout
            logout()
            st.rerun()
    
    st.divider()

# Main content
if not is_logged_in():
    st.warning("⚠️ Please log in to access the dashboard.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Log In", type="primary"):
            from app.services.auth_service import login_user
            try:
                success, message = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            except ValueError as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.subheader("📝 Register")
        new_username = st.text_input("Username", key="register_user")
        new_password = st.text_input("Password", type="password", key="register_pass")
        new_password_confirm = st.text_input("Confirm Password", type="password", key="register_pass_confirm")
        
        if st.button("Register", type="primary"):
            from app.services.auth_service import register_user
            
            if new_password != new_password_confirm:
                st.error("Passwords do not match")
            else:
                try:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                except ValueError as e:
                    st.error(f"Error: {e}")

else:
    # Dashboard content
    st.success(f"Welcome back, **{get_current_user()}**! 👋")
    
    tabs = st.tabs(["📊 Overview", "📈 Analytics", "🔍 Data Explorer"])
    
    with tabs[0]:
        st.subheader("Dashboard Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total Users", value="1,234")
        with col2:
            st.metric(label="Active Sessions", value="89")
        with col3:
            st.metric(label="Data Points", value="45,678")
        with col4:
            st.metric(label="Uptime", value="99.9%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("System Status")
            st.info("""
            ✅ **All Systems Operational**
            
            - Database: Connected
            - API: Responsive (avg 125ms)
            - Authentication: Active
            - Data Sync: Running
            """)
        
        with col2:
            st.subheader("Recent Activity")
            st.info("""
            📋 **Latest Events**
            
            - New user registered
            - Data import completed
            - Report generated
            - System check passed
            """)
    
    with tabs[1]:
        st.subheader("Analytics & Insights")
        
        st.markdown("### Sample Analytics")
        
        # Sample metrics
        metric_data = {
            "Metric": ["User Engagement", "Data Quality", "System Performance", "Security Score"],
            "Value": [87, 95, 92, 98],
            "Status": ["Good", "Excellent", "Good", "Excellent"]
        }
        
        df_metrics = pd.DataFrame(metric_data)
        st.dataframe(df_metrics, use_container_width=True)
        
        # Sample chart
        st.subheader("Trends Over Time")
        chart_data = pd.DataFrame(
            {
                "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "User Growth": [100, 120, 150, 180, 210, 250],
                "Data Volume": [1000, 1200, 1800, 2200, 2800, 3200]
            }
        )
        st.line_chart(chart_data.set_index("Month"))
    
    with tabs[2]:
        st.subheader("Data Explorer")
        
        st.markdown("### Load and Explore Datasets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dataset_name = st.text_input("Dataset Name", placeholder="e.g., incidents, tickets")
        
        with col2:
            if st.button("Load Dataset"):
                st.info(f"Dataset '{dataset_name}' would be loaded here")
        
        st.markdown("#### Sample Data")
        sample_df = pd.DataFrame(
            {
                "ID": [1, 2, 3, 4, 5],
                "Event": ["Login", "Data Export", "Report Gen", "System Check", "Backup"],
                "Timestamp": pd.date_range("2024-01-01", periods=5),
                "User": ["alice", "bob", "alice", "charlie", "admin"],
                "Status": ["Success", "Success", "Failed", "Success", "Success"]
            }
        )
        st.dataframe(sample_df, use_container_width=True)
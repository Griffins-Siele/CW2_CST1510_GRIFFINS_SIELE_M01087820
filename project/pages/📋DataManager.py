"""Data Manager Page - CRUD operations"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.session_state import is_logged_in, get_current_user
from app.data.models import AnalyticsRecord

st.set_page_config(page_title="Data Manager", page_icon="📋", layout="wide")

# Check authentication
if not is_logged_in():
    st.error("⚠️ Please log in first!")
    st.stop()

st.title("📋 Data Manager")

with st.sidebar:
    st.header("Navigation")
    st.success(f"✅ User: {get_current_user()}")
    if st.button("🚪 Logout"):
        from app.session_state import logout
        logout()
        st.rerun()

# Tabs for different operations
tabs = st.tabs(["View Data", "Upload Data", "Create Record", "Settings"])

with tabs[0]:
    st.subheader("View Dataset")
    
    dataset = st.selectbox(
        "Select Dataset",
        ["Cyber Incidents", "IT Tickets", "Users", "Analytics Records"]
    )
    
    # Sample data
    if dataset == "Cyber Incidents":
        df = pd.DataFrame({
            "ID": range(1, 6),
            "Date": pd.date_range("2024-01-01", periods=5),
            "Type": ["Phishing", "Malware", "DDoS", "Intrusion", "Data Breach"],
            "Severity": ["High", "Critical", "Critical", "High", "Medium"],
            "Status": ["Resolved", "In Progress", "Resolved", "In Progress", "Resolved"]
        })
    elif dataset == "IT Tickets":
        df = pd.DataFrame({
            "ID": range(1001, 1006),
            "Priority": ["High", "Critical", "Medium", "High", "Low"],
            "Status": ["Assigned", "In Progress", "Resolved", "Open", "On Hold"],
            "Assigned_To": ["tech1", "tech2", "tech1", "admin", "tech3"]
        })
    elif dataset == "Users":
        df = pd.DataFrame({
            "Username": ["alice", "bob", "charlie", "diana", "eve"],
            "Email": ["alice@ex.com", "bob@ex.com", "charlie@ex.com", "diana@ex.com", "eve@ex.com"],
            "Role": ["Analyst", "Admin", "Analyst", "User", "Analyst"],
            "Status": ["Active", "Active", "Active", "Inactive", "Active"]
        })
    else:  # Analytics Records
        df = pd.DataFrame({
            "ID": range(1, 6),
            "Title": ["User Growth", "API Response Time", "System Uptime", "Data Quality", "Security Score"],
            "Type": ["percentage", "milliseconds", "percentage", "percentage", "score"],
            "Value": [12.5, 125, 99.9, 95.2, 98.5]
        })
    
    st.dataframe(df, use_container_width=True)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label=f"Download {dataset} as CSV",
        data=csv,
        file_name=f"{dataset}.csv",
        mime="text/csv"
    )

with tabs[1]:
    st.subheader("Upload Data")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df.head())
        
        if st.button("Save to Database"):
            st.info("Data would be saved to database here (Week 8 integration)")

with tabs[2]:
    st.subheader("Create Analytics Record")
    
    col1, col2 = st.columns(2)
    
    with col1:
        record_id = st.number_input("Record ID", min_value=1, value=100)
        title = st.text_input("Record Title", placeholder="e.g., User Growth")
    
    with col2:
        metric_type = st.selectbox("Metric Type", ["percentage", "count", "milliseconds", "score"])
        value = st.number_input("Value", value=0.0)
    
    if st.button("Create Record", type="primary"):
        try:
            # Use OOP model from Week 11
            record = AnalyticsRecord(record_id, title, metric_type, value)
            st.success(f"✅ Record created: {record}")
        except ValueError as e:
            st.error(f"❌ Error: {e}")

with tabs[3]:
    st.subheader("Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Data Settings**")
        auto_refresh = st.checkbox("Auto-refresh data", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 10, 300, 60)
    
    with col2:
        st.markdown("**Display Settings**")
        rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100])
        date_format = st.selectbox("Date format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD-MM-YYYY"])
    
    if st.button("Save Settings"):
        st.success("✅ Settings saved!")

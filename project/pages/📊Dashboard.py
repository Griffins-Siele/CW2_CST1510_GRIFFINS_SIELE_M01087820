"""Dashboard Page - Data visualization (Week 9)"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.session_state import is_logged_in, get_current_user

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Check authentication
if not is_logged_in():
    st.error("⚠️ Please log in first!")
    st.stop()

st.title("📊 Executive Dashboard")

with st.sidebar:
    st.header("Navigation")
    st.success(f"✅ User: {get_current_user()}")
    if st.button("🚪 Logout"):
        from app.session_state import logout
        logout()
        st.rerun()
    
    # Filters
    st.divider()
    st.subheader("Filters")
    date_range = st.date_input("Select Date Range", value=[])
    severity_filter = st.multiselect(
        "Severity Level",
        ["Low", "Medium", "High", "Critical"],
        default=["High", "Critical"]
    )

# Dashboard metrics
st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Total Incidents", value="487")
with col2:
    st.metric(label="Critical", value="23")
with col3:
    st.metric(label="Resolved", value="412")
with col4:
    st.metric(label="Avg Response", value="2.4h")
with col5:
    st.metric(label="MTTR", value="4.8h")

st.divider()

# Charts
tab1, tab2, tab3, tab4 = st.tabs(["Incidents by Severity", "Status Distribution", "Timeline", "Top Analysts"])

with tab1:
    severity_data = pd.DataFrame({
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Count": [23, 145, 210, 109]
    })
    st.bar_chart(severity_data.set_index("Severity"))

with tab2:
    status_data = pd.DataFrame({
        "Status": ["Resolved", "In Progress", "Open", "On Hold"],
        "Count": [412, 34, 28, 13]
    })
    st.bar_chart(status_data.set_index("Status"))

with tab3:
    timeline_data = pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=30),
        "Incidents": np.random.randint(10, 30, 30),
        "Resolved": np.random.randint(5, 20, 30)
    })
    st.area_chart(timeline_data.set_index("Date"))

with tab4:
    analyst_data = pd.DataFrame({
        "Analyst": ["alice", "bob", "charlie", "diana"],
        "Resolved": [87, 64, 92, 58]
    })
    st.bar_chart(analyst_data.set_index("Analyst"))

st.divider()

st.subheader("Recent Incidents")
recent_incidents = pd.DataFrame({
    "Incident ID": [101, 102, 103, 104, 105],
    "Type": ["Phishing", "Malware", "DDoS", "SQL Injection", "Ransomware"],
    "Severity": ["High", "Critical", "Critical", "High", "Critical"],
    "Status": ["Resolved", "In Progress", "Resolved", "In Progress", "Resolved"],
    "Assigned To": ["alice", "bob", "charlie", "alice", "diana"],
    "Created": pd.date_range("2024-01-27", periods=5)
})

st.dataframe(recent_incidents, use_container_width=True)

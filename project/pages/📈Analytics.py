"""Analytics Page - Multi-page Streamlit app (Week 9)"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.session_state import is_logged_in, get_current_user

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

# Check authentication
if not is_logged_in():
    st.error("⚠️ Please log in first!")
    st.stop()

st.title("📈 Advanced Analytics")

with st.sidebar:
    st.header("Navigation")
    st.success(f"✅ User: {get_current_user()}")
    if st.button("🚪 Logout"):
        from app.session_state import logout
        logout()
        st.rerun()

# Analytics content
tabs = st.tabs(["Incidents", "Tickets", "Users", "Custom Analysis"])

with tabs[0]:
    st.subheader("Cyber Incidents Analytics")
    
    # Sample incident data
    incidents = pd.DataFrame({
        "ID": range(1, 11),
        "Date": pd.date_range("2024-01-01", periods=10),
        "Type": ["Malware", "Phishing", "DDoS", "Malware", "SQL Injection", 
                 "Phishing", "Ransomware", "Privilege Escalation", "Data Breach", "Malware"],
        "Severity": ["High", "Medium", "Critical", "High", "High", 
                     "Low", "Critical", "High", "Critical", "Medium"],
        "Status": ["Resolved", "In Progress", "Resolved", "Resolved", "In Progress",
                   "Resolved", "Resolved", "In Progress", "Resolved", "Resolved"],
        "Analyst": ["alice", "bob", "alice", "charlie", "bob", 
                    "alice", "charlie", "bob", "alice", "charlie"]
    })
    
    st.dataframe(incidents, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(incidents))
    with col2:
        critical = len(incidents[incidents["Severity"] == "Critical"])
        st.metric("Critical Issues", critical)
    with col3:
        resolved = len(incidents[incidents["Status"] == "Resolved"])
        st.metric("Resolved", f"{resolved}/{len(incidents)}")
    
    # Chart
    severity_counts = incidents["Severity"].value_counts()
    st.bar_chart(severity_counts)

with tabs[1]:
    st.subheader("IT Tickets Analytics")
    
    # Sample ticket data
    tickets = pd.DataFrame({
        "ID": range(1001, 1011),
        "Title": ["Server Down", "Network Issue", "Software Update", "Hardware Repair",
                  "Password Reset", "Access Request", "System Upgrade", "Bug Fix",
                  "Performance Issue", "Security Patch"],
        "Priority": ["High", "Critical", "Medium", "High", "Low", "Medium", "High", "Medium", "High", "Critical"],
        "Status": ["Assigned", "In Progress", "On Hold", "Resolved", "Open", 
                   "Assigned", "In Progress", "Resolved", "In Progress", "Assigned"],
        "Assigned_To": ["tech1", "tech2", "tech1", "tech3", "admin", 
                        "tech2", "tech1", "tech3", "tech2", "tech1"]
    })
    
    st.dataframe(tickets, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open Tickets", len(tickets[tickets["Status"] == "Open"]))
    with col2:
        in_progress = len(tickets[tickets["Status"] == "In Progress"])
        st.metric("In Progress", in_progress)
    with col3:
        st.metric("Total Tickets", len(tickets))

with tabs[2]:
    st.subheader("User Activity Analytics")
    
    # Sample user data
    users = pd.DataFrame({
        "Username": ["alice", "bob", "charlie", "diana", "eve"],
        "Email": ["alice@example.com", "bob@example.com", "charlie@example.com", 
                  "diana@example.com", "eve@example.com"],
        "Role": ["Analyst", "Admin", "Analyst", "User", "Analyst"],
        "Logins": [127, 89, 156, 34, 212],
        "Last_Login": pd.date_range("2024-01-01", periods=5, freq="D"),
        "Status": ["Active", "Active", "Active", "Inactive", "Active"]
    })
    
    st.dataframe(users, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(users))
    with col2:
        active = len(users[users["Status"] == "Active"])
        st.metric("Active Users", active)
    with col3:
        st.metric("Avg Logins", int(users["Logins"].mean()))

with tabs[3]:
    st.subheader("Custom Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Time Series", "Distribution", "Correlation", "Comparison"]
    )
    
    if analysis_type == "Time Series":
        st.line_chart({
            "Events": np.cumsum(np.random.randint(0, 10, 30)),
            "Alerts": np.cumsum(np.random.randint(0, 5, 30))
        })
    elif analysis_type == "Distribution":
        st.bar_chart(np.random.randn(30).cumsum())
    elif analysis_type == "Correlation":
        st.write("Correlation matrix would be displayed here")
        corr_data = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])
        st.dataframe(corr_data.corr())
    else:
        st.write("Comparison analysis would be displayed here")

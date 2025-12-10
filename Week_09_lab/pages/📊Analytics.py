import streamlit as st
import pandas as pd
import numpy as np
from session_state import init_session
from pathlib import Path

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

init_session()

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.title("📊 Analytics Dashboard")
st.success(f"Logged in as: **{st.session_state.username}**")

# Load IT tickets data for analytics
data_path = Path(__file__).parent.parent / "DATA" / "it_tickets.csv"

if data_path.exists():
    df = pd.read_csv(data_path)
else:
    # Create sample data
    df = pd.DataFrame({
        "ticket_id": [f"TCK-{1001+i}" for i in range(15)],
        "title": ["Email outage", "Network down", "Password reset", "Printer error", "Software update",
                  "Email outage", "Network down", "Password reset", "Printer error", "Software update",
                  "Email outage", "Network down", "Password reset", "Printer error", "Software update"],
        "priority": np.random.choice(["High", "Medium", "Low"], 15),
        "status": np.random.choice(["Open", "In Progress", "Closed"], 15),
        "assignee": np.random.choice(["Griffins", "Siele", "Alice", "Diana"], 15),
        "created_date": pd.date_range("2025-11-01", periods=15, freq="D").astype(str)
    })

st.subheader("Ticket Statistics")

# KPI metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Tickets",
        value=len(df),
    )

with col2:
    high_priority = len(df[df["priority"] == "High"])
    st.metric(
        label="High Priority",
        value=high_priority,
    )

with col3:
    open_tickets = len(df[df["status"] == "Open"])
    st.metric(
        label="Open Tickets",
        value=open_tickets,
    )

with col4:
    closed_tickets = len(df[df["status"] == "Closed"])
    st.metric(
        label="Closed Tickets",
        value=closed_tickets,
    )

st.divider()

# Visualizations
tab_overview, tab_priority, tab_assignee = st.tabs(["📈 Overview", "🎯 Priority Analysis", "👥 Assignee Analysis"])

with tab_overview:
    st.subheader("Ticket Status Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        status_counts = df["status"].value_counts()
        st.bar_chart(status_counts)
    
    with col2:
        st.write("**Status Summary**")
        for status, count in status_counts.items():
            st.write(f"- {status}: {count}")

with tab_priority:
    st.subheader("Priority Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        priority_counts = df["priority"].value_counts()
        st.bar_chart(priority_counts)
    
    with col2:
        st.write("**Priority Breakdown**")
        for priority in ["High", "Medium", "Low"]:
            count = len(df[df["priority"] == priority])
            pct = round(100 * count / len(df), 1)
            st.write(f"- {priority}: {count} ({pct}%)")

with tab_assignee:
    st.subheader("Workload by Assignee")
    
    assignee_counts = df["assignee"].value_counts()
    st.bar_chart(assignee_counts)
    
    st.write("**Assignee Workload**")
    for assignee, count in assignee_counts.items():
        st.write(f"- {assignee}: {count} tickets")

st.divider()

st.subheader("Detailed Ticket Data")

# Filter controls
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    status_filter = st.multiselect(
        "Filter by Status:",
        options=df["status"].unique(),
        default=df["status"].unique()
    )

with col_filter2:
    priority_filter = st.multiselect(
        "Filter by Priority:",
        options=df["priority"].unique(),
        default=df["priority"].unique()
    )

# Apply filters
filtered_df = df[
    (df["status"].isin(status_filter)) & 
    (df["priority"].isin(priority_filter))
]

st.dataframe(filtered_df, use_container_width=True)

st.divider()

st.subheader("Export Options")
col_export1, col_export2 = st.columns(2)

with col_export1:
    if st.button("Export as CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="tickets_report.csv",
            mime="text/csv"
        )

with col_export2:
    if st.button("Export as JSON"):
        json = filtered_df.to_json(orient="records", indent=2)
        st.download_button(
            label="Download JSON",
            data=json,
            file_name="tickets_report.json",
            mime="application/json"
        )

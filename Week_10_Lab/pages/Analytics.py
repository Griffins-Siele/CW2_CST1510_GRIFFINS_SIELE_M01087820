"""Analytics Dashboard: IT Tickets Analysis with AI Assistant."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from session_state import init_session
from ai_helper import (
    explain_statistics, 
    streamlit_ai_chat,
    is_openai_configured
)
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session()

# Authentication check
if not st.session_state.logged_in:
    st.error(" You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.title(" Analytics Dashboard - IT Tickets")
st.success(f"Logged in as: **{st.session_state.username}**")

# Load data
data_path = Path(__file__).parent.parent / "DATA" / "it_tickets.csv"

try:
    if data_path.exists():
        df = pd.read_csv(data_path)
        st.info(f"📁 Loaded {len(df)} tickets from database")
    else:
        # Create sample data
        df = pd.DataFrame({
            "ticket_id": [f"TCK-{1001+i}" for i in range(20)],
            "title": np.random.choice([
                "Email outage", "Network down", "Password reset", "Printer error",
                "Software update", "Hardware issue", "VPN access", "License renewal",
                "Backup failure", "Malware alert"
            ], 20),
            "priority": np.random.choice(["High", "Medium", "Low"], 20),
            "status": np.random.choice(["Open", "In Progress", "Closed"], 20),
            "category": np.random.choice(["Network", "Hardware", "Software", "Security"], 20),
            "assignee": np.random.choice(["Griffins", "Siele", "Alice", "Diana"], 20),
            "created_date": pd.date_range("2025-11-01", periods=20, freq="D").astype(str)
        })
        st.warning("📁 Sample data created (no CSV file found)")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.header(" Filters")

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

priority_filter = st.sidebar.multiselect(
    "Filter by Priority",
    options=df["priority"].unique(),
    default=df["priority"].unique()
)

if "category" in df.columns:
    category_filter = st.sidebar.multiselect(
        "Filter by Category",
        options=df["category"].unique(),
        default=df["category"].unique()
    )
else:
    category_filter = []

# Apply filters
filtered_df = df[
    (df["status"].isin(status_filter)) & 
    (df["priority"].isin(priority_filter))
]

if category_filter and "category" in df.columns:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

st.divider()

# ===== KEY METRICS =====
st.subheader(" Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_tickets = len(filtered_df)
    st.metric(
        label="Total Tickets",
        value=total_tickets,
        delta=f"Active: {len(filtered_df[filtered_df['status'] != 'Closed'])}"
    )

with col2:
    high_priority = len(filtered_df[filtered_df["priority"] == "High"])
    pct = round(100 * high_priority / len(filtered_df), 1) if len(filtered_df) > 0 else 0
    st.metric(
        label="High Priority",
        value=high_priority,
        delta=f"{pct}% of total"
    )

with col3:
    open_tickets = len(filtered_df[filtered_df["status"] == "Open"])
    st.metric(
        label="Open Tickets",
        value=open_tickets,
        delta=f"{round(100*open_tickets/len(filtered_df), 1) if len(filtered_df) > 0 else 0}%"
    )

with col4:
    closed_tickets = len(filtered_df[filtered_df["status"] == "Closed"])
    st.metric(
        label="Closed Tickets",
        value=closed_tickets,
        delta=f"Completion: {round(100*closed_tickets/len(filtered_df), 1) if len(filtered_df) > 0 else 0}%"
    )

st.divider()

# ===== VISUALIZATIONS =====
tab_overview, tab_priority, tab_assignee, tab_details = st.tabs(
    [" Overview", " Priority", " Assignees", " Details"]
)

with tab_overview:
    st.subheader("Ticket Status Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(filtered_df) > 0:
            status_counts = filtered_df["status"].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={"x": "Status", "y": "Count"},
                title="Tickets by Status",
                color=status_counts.index
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data to display")
    
    with col2:
        st.write("**Status Summary**")
        if len(filtered_df) > 0:
            for status, count in filtered_df["status"].value_counts().items():
                st.write(f"• {status}: {count} tickets")
        else:
            st.info("No tickets")

with tab_priority:
    st.subheader("Priority Distribution & Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(filtered_df) > 0:
            priority_counts = filtered_df["priority"].value_counts()
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Priority Distribution",
                color_discrete_map={"High": "#FF6B6B", "Medium": "#FFA500", "Low": "#51CF66"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data to display")
    
    with col2:
        st.write("**Priority Breakdown**")
        if len(filtered_df) > 0:
            for priority in ["High", "Medium", "Low"]:
                count = len(filtered_df[filtered_df["priority"] == priority])
                pct = round(100 * count / len(filtered_df), 1)
                st.write(f"• {priority}: {count} ({pct}%)")
        else:
            st.info("No tickets")

with tab_assignee:
    st.subheader("Workload by Assignee")
    
    if len(filtered_df) > 0 and "assignee" in filtered_df.columns:
        assignee_counts = filtered_df["assignee"].value_counts().reset_index()
        assignee_counts.columns = ["Assignee", "Count"]
        fig = px.bar(
            assignee_counts,
            x="Assignee",
            y="Count",
            title="Tickets per Assignee",
            color="Count",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Assignee Workload**")
        for assignee, count in assignee_counts.items():
            st.write(f"• {assignee}: {count} tickets")
    else:
        st.info("No assignee data available")

with tab_details:
    st.subheader("Detailed Ticket Data")
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label=" Download CSV",
            data=csv,
            file_name="tickets_analytics.csv",
            mime="text/csv"
        )
    
    with col2:
        json = filtered_df.to_json(orient="records", indent=2)
        st.download_button(
            label=" Download JSON",
            data=json,
            file_name="tickets_analytics.json",
            mime="application/json"
        )

st.divider()

# ===== AI ASSISTANT SECTION =====
st.subheader(" AI Assistant - Statistics Insights")

if is_openai_configured():
    with st.expander(" Ask AI about ticket statistics", expanded=True):
        col_info, col_ask = st.columns([1, 2])
        
        with col_info:
            st.info("""
            **Available Analysis:**
            - Trend insights
            - Priority patterns
            - Workload distribution
            - Resolution recommendations
            """)
        
        with col_ask:
            user_question = st.text_area(
                "Ask a question about the ticket data:",
                placeholder="E.g., What patterns do you see in high priority tickets?",
                height=100,
                key="ai_ticket_question"
            )
            
            if st.button(" Get AI Insights", type="primary"):
                if user_question:
                    data_summary = f"""
                    Total Tickets: {len(filtered_df)}
                    Open: {len(filtered_df[filtered_df['status'] == 'Open'])}
                    In Progress: {len(filtered_df[filtered_df['status'] == 'In Progress'])}
                    Closed: {len(filtered_df[filtered_df['status'] == 'Closed'])}
                    High Priority: {len(filtered_df[filtered_df['priority'] == 'High'])}
                    Medium Priority: {len(filtered_df[filtered_df['priority'] == 'Medium'])}
                    Low Priority: {len(filtered_df[filtered_df['priority'] == 'Low'])}
                    
                    User Question: {user_question}
                    """
                    
                    success, response = explain_statistics(data_summary)
                    
                    if success:
                        st.success(" AI Analysis Complete")
                        st.write(response)
                    else:
                        st.error(f" Error: {response}")
                else:
                    st.warning("Please enter a question.")
else:
    st.warning("""
     **AI Assistant Not Available**
    
    To enable AI features, set the `OPENAI_API_KEY` environment variable:
    ```
    $env:OPENAI_API_KEY = "your-api-key-here"
    ```
    
    Then restart the application.
    """)

st.divider()

# Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Data Manager", use_container_width=True):
        st.switch_page("pages/DataManager.py")

with col2:
    if st.button(" Incidents", use_container_width=True):
        st.switch_page("pages/Incidents.py")

with col3:
    if st.button(" Metadata", use_container_width=True):
        st.switch_page("pages/Metadata.py")

with col4:
    if st.button(" Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

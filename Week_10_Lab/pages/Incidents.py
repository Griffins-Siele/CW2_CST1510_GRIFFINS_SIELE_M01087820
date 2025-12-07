"""Cyber Incidents Dashboard - Tier 2 Secondary Domain."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from session_state import init_session
from ai_helper import get_security_advice, is_openai_configured
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Incidents",
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

st.title(" Cyber Incidents Dashboard")
st.success(f"Logged in as: **{st.session_state.username}**")

# Load data
data_path = Path(__file__).parent.parent / "DATA" / "cyber_incidents.csv"

try:
    if data_path.exists():
        df = pd.read_csv(data_path)
        st.info(f"📁 Loaded {len(df)} incidents from database")
    else:
        # Create sample cyber incidents data
        incident_types = [
            "Malware", "Phishing", "Data Breach", "DDoS", "Ransomware",
            "SQL Injection", "XSS Attack", "Brute Force", "Insider Threat",
            "Zero-Day", "Privilege Escalation", "Social Engineering"
        ]
        
        severities = ["Critical", "High", "Medium", "Low"]
        statuses = ["Detected", "Investigating", "Contained", "Resolved", "Escalated"]
        departments = ["IT", "Finance", "HR", "Operations", "Security"]
        
        df = pd.DataFrame({
            "incident_id": [f"INC-{2001+i}" for i in range(25)],
            "incident_type": np.random.choice(incident_types, 25),
            "severity": np.random.choice(severities, 25),
            "status": np.random.choice(statuses, 25),
            "detected_date": pd.date_range("2025-10-01", periods=25, freq="D").astype(str),
            "affected_systems": np.random.choice(["Web Server", "Database", "Email", "VPN", "Workstations"], 25),
            "affected_department": np.random.choice(departments, 25),
            "response_time_hours": np.random.randint(1, 48, 25)
        })
        
        st.warning("📁 Sample cyber incidents data created (no CSV file found)")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.header(" Filters")

severity_filter = st.sidebar.multiselect(
    "Filter by Severity",
    options=["Critical", "High", "Medium", "Low"],
    default=["Critical", "High", "Medium", "Low"]
)

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["status"].unique() if "status" in df.columns else [],
    default=df["status"].unique() if "status" in df.columns else []
)

incident_type_filter = st.sidebar.multiselect(
    "Filter by Type",
    options=df["incident_type"].unique() if "incident_type" in df.columns else [],
    default=df["incident_type"].unique() if "incident_type" in df.columns else []
)

# Apply filters
filtered_df = df.copy()

if "severity" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]

if "status" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]

if "incident_type" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["incident_type"].isin(incident_type_filter)]

st.divider()

# ===== KEY METRICS =====
st.subheader(" Incident Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Incidents",
        value=len(filtered_df),
        delta=f"Period: {len(df)} total"
    )

with col2:
    critical_count = len(filtered_df[filtered_df["severity"] == "Critical"]) if "severity" in filtered_df.columns else 0
    st.metric(
        label="Critical 🚨",
        value=critical_count,
        delta="Requires attention"
    )

with col3:
    high_count = len(filtered_df[filtered_df["severity"] == "High"]) if "severity" in filtered_df.columns else 0
    st.metric(
        label="High 🔴",
        value=high_count,
        delta="Monitor closely"
    )

with col4:
    resolved_count = len(filtered_df[filtered_df["status"] == "Resolved"]) if "status" in filtered_df.columns else 0
    st.metric(
        label="Resolved ",
        value=resolved_count,
        delta=f"MTTR: Monitor"
    )

with col5:
    avg_response = filtered_df["response_time_hours"].mean() if "response_time_hours" in filtered_df.columns else 0
    st.metric(
        label="Avg Response Time",
        value=f"{avg_response:.1f}h",
        delta="Hours to initial response"
    )

st.divider()

# ===== VISUALIZATIONS =====
tab_severity, tab_type, tab_timeline, tab_affected = st.tabs(
    ["🔴 Severity Analysis", " Incident Types", "📅 Timeline", "💻 Affected Assets"]
)

with tab_severity:
    st.subheader("Severity Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(filtered_df) > 0 and "severity" in filtered_df.columns:
            severity_counts = filtered_df["severity"].value_counts()
            severity_order = ["Critical", "High", "Medium", "Low"]
            severity_counts = severity_counts.reindex([s for s in severity_order if s in severity_counts.index])
            
            color_map = {"Critical": "#FF0000", "High": "#FF6B6B", "Medium": "#FFA500", "Low": "#51CF66"}
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Incidents by Severity",
                labels={"x": "Severity", "y": "Count"},
                color=severity_counts.index,
                color_discrete_map=color_map
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No severity data available")
    
    with col2:
        st.write("**Severity Breakdown**")
        if len(filtered_df) > 0 and "severity" in filtered_df.columns:
            for severity in ["Critical", "High", "Medium", "Low"]:
                count = len(filtered_df[filtered_df["severity"] == severity])
                if count > 0:
                    pct = round(100 * count / len(filtered_df), 1)
                    st.write(f"• {severity}: {count} ({pct}%)")

with tab_type:
    st.subheader("Incident Types Analysis")
    
    if len(filtered_df) > 0 and "incident_type" in filtered_df.columns:
        incident_counts = filtered_df["incident_type"].value_counts().reset_index()
        incident_counts.columns = ["Type", "Count"]
        
        fig = px.bar(
            incident_counts,
            y="Type",
            x="Count",
            orientation="h",
            title="Top Incident Types",
            color="Count",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No incident type data available")

with tab_timeline:
    st.subheader("Incident Timeline")
    
    if len(filtered_df) > 0 and "detected_date" in filtered_df.columns:
        timeline_data = filtered_df["detected_date"].value_counts().sort_index()
        
        fig = px.line(
            x=timeline_data.index,
            y=timeline_data.values,
            title="Incidents Over Time",
            labels={"x": "Date", "y": "Incident Count"},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available")

with tab_affected:
    st.subheader("Affected Systems & Departments")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(filtered_df) > 0 and "affected_systems" in filtered_df.columns:
            st.write("**Systems Affected**")
            systems = filtered_df["affected_systems"].value_counts()
            fig = px.pie(
                values=systems.values,
                names=systems.index,
                title="Incidents by System"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No system data available")
    
    with col2:
        if len(filtered_df) > 0 and "affected_department" in filtered_df.columns:
            st.write("**Departments Affected**")
            depts = filtered_df["affected_department"].value_counts()
            fig = px.pie(
                values=depts.values,
                names=depts.index,
                title="Incidents by Department"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No department data available")

st.divider()

# ===== DETAILED INCIDENT DATA =====
st.subheader(" Incident Details")

st.dataframe(filtered_df, use_container_width=True, height=400)

st.divider()

# ===== AI SECURITY ADVISOR =====
st.subheader(" AI Security Advisor")

if is_openai_configured():
    with st.expander(" Get Security Advice & Recommendations", expanded=True):
        st.info("Get AI-powered security advice for incidents and recommendations for prevention.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Quick preset incidents
            st.write("**Quick Scenarios:**")
            
            incident_scenario = st.radio(
                "Select scenario or enter custom:",
                [
                    "Custom scenario",
                    "Malware detection",
                    "Phishing campaign",
                    "Data breach",
                    "DDoS attack",
                    "Ransomware infection"
                ],
                key="incident_radio"
            )
        
        with col2:
            if incident_scenario == "Custom scenario":
                user_incident = st.text_area(
                    "Describe the security incident:",
                    placeholder="E.g., We detected suspicious login attempts from multiple IPs...",
                    height=120,
                    key="custom_incident"
                )
            else:
                user_incident = incident_scenario
            
            if st.button(" Get Security Advice", type="primary", use_container_width=True):
                if user_incident:
                    with st.spinner("Analyzing incident..."):
                        success, advice = get_security_advice(user_incident)
                        
                        if success:
                            st.success(" Security Advice Generated")
                            st.write(advice)
                        else:
                            st.error(f" Error: {advice}")
                else:
                    st.warning("Please describe an incident or select a scenario.")

else:
    st.warning("""
     **AI Security Advisor Not Available**
    
    To enable AI features, set the `OPENAI_API_KEY` environment variable:
    ```
    $env:OPENAI_API_KEY = "your-api-key-here"
    ```
    """)

st.divider()

# ===== INCIDENT RESPONSE GUIDE =====
with st.expander("📖 Incident Response Guide", expanded=False):
    st.markdown("""
    ### Incident Response Procedure
    
    1. **Detection & Alert**
       - Monitor security logs and alerts
       - Verify incident authenticity
       - Document initial findings
    
    2. **Containment**
       - Isolate affected systems
       - Preserve evidence
       - Limit lateral movement
    
    3. **Investigation**
       - Gather forensic evidence
       - Determine scope and impact
       - Identify root cause
    
    4. **Eradication**
       - Remove malware/threats
       - Patch vulnerabilities
       - Strengthen defenses
    
    5. **Recovery**
       - Restore systems from clean backups
       - Test before returning to production
       - Monitor for re-infection
    
    6. **Post-Incident**
       - Document lessons learned
       - Update security policies
       - Communicate with stakeholders
    """)

st.divider()

# Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")

with col2:
    if st.button(" Metadata", use_container_width=True):
        st.switch_page("pages/Metadata.py")

with col3:
    if st.button(" Users", use_container_width=True):
        st.switch_page("pages/Users.py")

with col4:
    if st.button(" Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

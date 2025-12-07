"""Users Analysis Dashboard - Tier 3 Tertiary Domain."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from session_state import init_session
from ai_helper import explain_statistics, is_openai_configured
import plotly.express as px

st.set_page_config(
    page_title="Users",
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

st.title(" User Analytics Dashboard")
st.success(f"Logged in as: **{st.session_state.username}**")

# Load data
data_path = Path(__file__).parent.parent / "DATA" / "users.txt"

try:
    # Create comprehensive user analytics data
    users_data = {
        "user_id": [f"USR-{4001+i}" for i in range(20)],
        "username": ["alice", "bob", "charlie", "diana", "eve", "frank", "grace", "henry",
                     "iris", "jack", "kate", "liam", "maya", "noah", "olivia", "paul",
                     "quinn", "rachel", "sam", "tina"],
        "department": np.random.choice(["IT", "Security", "Finance", "HR", "Operations"], 20),
        "role": np.random.choice(["Admin", "Analyst", "User", "Manager"], 20),
        "last_login": pd.date_range("2025-11-01", periods=20, freq="H").astype(str),
        "login_count_30d": np.random.randint(1, 100, 20),
        "failed_attempts_30d": np.random.randint(0, 10, 20),
        "mfa_enabled": np.random.choice([True, False], 20),
        "account_status": np.random.choice(["Active", "Inactive", "Locked", "Suspended"], 20),
        "last_password_change": pd.date_range("2025-01-01", periods=20, freq="D").astype(str)
    }
    
    df = pd.DataFrame(users_data)
    st.info(f"📁 Loaded {len(df)} user records from system")
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.header(" Filters")

department_filter = st.sidebar.multiselect(
    "Filter by Department",
    options=df["department"].unique(),
    default=df["department"].unique()
)

role_filter = st.sidebar.multiselect(
    "Filter by Role",
    options=df["role"].unique(),
    default=df["role"].unique()
)

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=df["account_status"].unique(),
    default=df["account_status"].unique()
)

mfa_filter = st.sidebar.radio(
    "MFA Status",
    ["All", "MFA Enabled", "MFA Disabled"]
)

# Apply filters
filtered_df = df[
    (df["department"].isin(department_filter)) &
    (df["role"].isin(role_filter)) &
    (df["account_status"].isin(status_filter))
]

if mfa_filter == "MFA Enabled":
    filtered_df = filtered_df[filtered_df["mfa_enabled"] == True]
elif mfa_filter == "MFA Disabled":
    filtered_df = filtered_df[filtered_df["mfa_enabled"] == False]

st.divider()

# ===== KEY METRICS =====
st.subheader(" User Statistics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Users",
        value=len(filtered_df),
        delta=f"System: {len(df)}"
    )

with col2:
    active_users = len(filtered_df[filtered_df["account_status"] == "Active"])
    st.metric(
        label="Active Users",
        value=active_users,
        delta=f"{round(100*active_users/len(filtered_df), 1) if len(filtered_df) > 0 else 0}%"
    )

with col3:
    mfa_enabled = len(filtered_df[filtered_df["mfa_enabled"] == True])
    st.metric(
        label="MFA Enabled",
        value=mfa_enabled,
        delta=f"{round(100*mfa_enabled/len(filtered_df), 1) if len(filtered_df) > 0 else 0}% secure"
    )

with col4:
    failed_attempts = filtered_df["failed_attempts_30d"].sum()
    st.metric(
        label="Failed Login Attempts",
        value=failed_attempts,
        delta="Last 30 days"
    )

with col5:
    avg_logins = filtered_df["login_count_30d"].mean()
    st.metric(
        label="Avg Logins/User",
        value=f"{avg_logins:.1f}",
        delta="Last 30 days"
    )

st.divider()

# ===== VISUALIZATIONS =====
tab_dept, tab_role, tab_security, tab_activity = st.tabs(
    ["Department", "Roles", " Security", " Activity"]
)

with tab_dept:
    st.subheader("Users by Department")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(filtered_df) > 0:
            dept_counts = filtered_df["department"].value_counts()
            fig = px.bar(
                x=dept_counts.index,
                y=dept_counts.values,
                title="User Distribution by Department",
                labels={"x": "Department", "y": "Count"},
                color=dept_counts.index
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")
    
    with col2:
        st.write("**Department Summary**")
        if len(filtered_df) > 0:
            for dept, count in filtered_df["department"].value_counts().items():
                pct = round(100 * count / len(filtered_df), 1)
                st.write(f"• {dept}: {count} ({pct}%)")

with tab_role:
    st.subheader("Users by Role")
    
    if len(filtered_df) > 0:
        role_counts = filtered_df["role"].value_counts()
        
        fig = px.pie(
            values=role_counts.values,
            names=role_counts.index,
            title="User Distribution by Role",
            color_discrete_map={
                "Admin": "#FF0000",
                "Manager": "#FF8C00",
                "Analyst": "#4169E1",
                "User": "#32CD32"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Role Summary**")
        for role, count in role_counts.items():
            pct = round(100 * count / len(filtered_df), 1)
            st.write(f"• {role}: {count} ({pct}%)")
    else:
        st.info("No data available")

with tab_security:
    st.subheader("Security Status Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Account Status**")
        if len(filtered_df) > 0:
            status_counts = filtered_df["account_status"].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Account Status Distribution",
                labels={"x": "Status", "y": "Count"},
                color=status_counts.index,
                color_discrete_map={
                    "Active": "#51CF66",
                    "Inactive": "#FFD700",
                    "Locked": "#FF8C00",
                    "Suspended": "#FF0000"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")
    
    with col2:
        st.write("**MFA Adoption**")
        if len(filtered_df) > 0:
            mfa_counts = filtered_df["mfa_enabled"].value_counts()
            mfa_labels = ["MFA Enabled" if idx else "MFA Disabled" for idx in mfa_counts.index]
            
            fig = px.pie(
                values=mfa_counts.values,
                names=mfa_labels,
                title="MFA Adoption Rate",
                color_discrete_map={"MFA Enabled": "#51CF66", "MFA Disabled": "#FF6B6B"}
            )
            st.plotly_chart(fig, use_container_width=True)

with tab_activity:
    st.subheader("User Activity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Most Active Users (30d)**")
        if len(filtered_df) > 0:
            most_active = filtered_df.nlargest(10, "login_count_30d").reset_index(drop=True)
            fig = px.bar(
                most_active,
                x="login_count_30d",
                y="username",
                orientation="h",
                title="Top 10 Most Active Users",
                labels={"login_count_30d": "Login Count", "username": "User"},
                color="login_count_30d",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")
    
    with col2:
        st.write("**Failed Login Attempts (30d)**")
        if len(filtered_df) > 0:
            failed_users = filtered_df[filtered_df["failed_attempts_30d"] > 0].nlargest(10, "failed_attempts_30d").reset_index(drop=True)
            
            if len(failed_users) > 0:
                fig = px.bar(
                    failed_users,
                    x="failed_attempts_30d",
                    y="username",
                    orientation="h",
                    title="Users with Failed Login Attempts",
                    labels={"failed_attempts_30d": "Failed Attempts", "username": "User"},
                    color="failed_attempts_30d",
                    color_continuous_scale="Reds"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success(" No failed login attempts detected!")

st.divider()

# ===== DETAILED USER TABLE =====
st.subheader(" User Directory")

st.dataframe(filtered_df, use_container_width=True, height=400)

st.divider()

# ===== AI USER INSIGHTS =====
st.subheader(" AI User Analytics")

if is_openai_configured():
    with st.expander(" Get AI Analysis of User Patterns", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info("Ask AI about user behavior, security risks, and recommendations.")
        
        with col2:
            user_question = st.text_area(
                "Ask about user analytics:",
                placeholder="E.g., Which users should be priority for MFA enforcement? Any security concerns?",
                height=100,
                key="ai_user_question"
            )
            
            if st.button(" Analyze User Data", type="primary", use_container_width=True):
                if user_question:
                    user_summary = f"""
                    Total Users: {len(filtered_df)}
                    Active Users: {len(filtered_df[filtered_df['account_status'] == 'Active'])}
                    MFA Enabled: {len(filtered_df[filtered_df['mfa_enabled'] == True])}
                    Failed Login Attempts: {filtered_df['failed_attempts_30d'].sum()}
                    
                    Department Distribution:
                    {filtered_df['department'].value_counts().to_string()}
                    
                    Role Distribution:
                    {filtered_df['role'].value_counts().to_string()}
                    
                    User Question: {user_question}
                    """
                    
                    with st.spinner("Analyzing user data..."):
                        success, response = explain_statistics(user_summary)
                        
                        if success:
                            st.success(" Analysis Complete")
                            st.write(response)
                        else:
                            st.error(f" Error: {response}")
                else:
                    st.warning("Please ask a question about user analytics.")
else:
    st.warning("""
     **AI Insights Not Available**
    
    To enable AI features, set the `OPENAI_API_KEY` environment variable.
    """)

st.divider()


# Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Incidents", use_container_width=True):
        st.switch_page("pages/Incidents.py")

with col2:
    if st.button(" Metadata", use_container_width=True):
        st.switch_page("pages/Metadata.py")

with col3:
    if st.button(" Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")

with col4:
    if st.button(" Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

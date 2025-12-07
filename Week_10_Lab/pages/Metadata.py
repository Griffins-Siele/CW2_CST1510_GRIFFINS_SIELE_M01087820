"""Data Metadata Dashboard - Tier 2 Secondary Domain."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from session_state import init_session
from ai_helper import explain_statistics, is_openai_configured
import plotly.express as px

st.set_page_config(
    page_title="Metadata",
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

st.title(" Data Metadata Dashboard")
st.success(f"Logged in as: **{st.session_state.username}**")

# Load data
data_path = Path(__file__).parent.parent / "DATA" / "datasets_metadata.csv"

try:
    if data_path.exists():
        df = pd.read_csv(data_path)
        st.info(f"📁 Loaded {len(df)} datasets from metadata catalog")
    else:
        # Create sample metadata
        df = pd.DataFrame({
            "dataset_id": [f"DS-{3001+i}" for i in range(15)],
            "dataset_name": [
                "IT Tickets", "Cyber Incidents", "User Profiles", "Network Traffic",
                "System Logs", "Access Logs", "Backup Status", "License Data",
                "Hardware Inventory", "Software Catalog", "Performance Metrics",
                "Security Events", "Compliance Reports", "Audit Logs", "Incident Response"
            ],
            "owner": np.random.choice(["IT Dept", "Security", "Operations", "Finance"], 15),
            "record_count": np.random.randint(100, 10000, 15),
            "size_mb": np.random.randint(10, 1000, 15),
            "last_updated": pd.date_range("2025-01-01", periods=15, freq="D").astype(str),
            "data_quality": np.random.choice(["Excellent", "Good", "Fair", "Poor"], 15),
            "sensitivity": np.random.choice(["Public", "Internal", "Confidential", "Restricted"], 15),
            "access_count_7d": np.random.randint(10, 500, 15)
        })
        
        st.warning("📁 Sample metadata created (no CSV file found)")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.header(" Filters")

owner_filter = st.sidebar.multiselect(
    "Filter by Owner",
    options=df["owner"].unique() if "owner" in df.columns else [],
    default=df["owner"].unique() if "owner" in df.columns else []
)

sensitivity_filter = st.sidebar.multiselect(
    "Filter by Sensitivity",
    options=df["sensitivity"].unique() if "sensitivity" in df.columns else [],
    default=df["sensitivity"].unique() if "sensitivity" in df.columns else []
)

quality_filter = st.sidebar.multiselect(
    "Filter by Quality",
    options=df["data_quality"].unique() if "data_quality" in df.columns else [],
    default=df["data_quality"].unique() if "data_quality" in df.columns else []
)

# Apply filters
filtered_df = df.copy()

if "owner" in filtered_df.columns and owner_filter:
    filtered_df = filtered_df[filtered_df["owner"].isin(owner_filter)]

if "sensitivity" in filtered_df.columns and sensitivity_filter:
    filtered_df = filtered_df[filtered_df["sensitivity"].isin(sensitivity_filter)]

if "data_quality" in filtered_df.columns and quality_filter:
    filtered_df = filtered_df[filtered_df["data_quality"].isin(quality_filter)]

st.divider()

# ===== KEY METRICS =====
st.subheader(" Metadata Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Datasets",
        value=len(filtered_df),
        delta=f"In catalog: {len(df)}"
    )

with col2:
    total_records = filtered_df["record_count"].sum() if "record_count" in filtered_df.columns else 0
    st.metric(
        label="Total Records",
        value=f"{total_records:,}",
        delta="Across datasets"
    )

with col3:
    total_size = filtered_df["size_mb"].sum() if "size_mb" in filtered_df.columns else 0
    st.metric(
        label="Total Size",
        value=f"{total_size} MB",
        delta=f"{total_size/1024:.1f} GB"
    )

with col4:
    excellent_quality = len(filtered_df[filtered_df["data_quality"] == "Excellent"]) if "data_quality" in filtered_df.columns else 0
    st.metric(
        label="Excellent Quality",
        value=excellent_quality,
        delta=f"{round(100*excellent_quality/len(filtered_df), 1) if len(filtered_df) > 0 else 0}%"
    )

with col5:
    total_access = filtered_df["access_count_7d"].sum() if "access_count_7d" in filtered_df.columns else 0
    avg_access = total_access / len(filtered_df) if len(filtered_df) > 0 else 0
    st.metric(
        label="Avg Access (7d)",
        value=f"{avg_access:.0f}",
        delta="Per dataset"
    )

st.divider()

# ===== VISUALIZATIONS =====
tab_quality, tab_sensitivity, tab_size, tab_access = st.tabs(
    [" Quality", " Sensitivity", " Size", " Access Patterns"]
)

with tab_quality:
    st.subheader("Data Quality Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(filtered_df) > 0 and "data_quality" in filtered_df.columns:
            quality_counts = filtered_df["data_quality"].value_counts()
            color_map = {"Excellent": "#51CF66", "Good": "#FFA500", "Fair": "#FFD700", "Poor": "#FF6B6B"}
            
            fig = px.bar(
                x=quality_counts.index,
                y=quality_counts.values,
                title="Datasets by Quality",
                labels={"x": "Quality", "y": "Count"},
                color=quality_counts.index,
                color_discrete_map=color_map
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No quality data available")
    
    with col1:
        if len(filtered_df) > 0 and "data_quality" in filtered_df.columns:
            st.write("**Quality Breakdown**")
            for quality in ["Excellent", "Good", "Fair", "Poor"]:
                count = len(filtered_df[filtered_df["data_quality"] == quality])
                if count > 0:
                    pct = round(100 * count / len(filtered_df), 1)
                    st.write(f"• {quality}: {count} ({pct}%)")

with tab_sensitivity:
    st.subheader("Data Sensitivity Classification")
    
    if len(filtered_df) > 0 and "sensitivity" in filtered_df.columns:
        sensitivity_counts = filtered_df["sensitivity"].value_counts()
        
        fig = px.pie(
            values=sensitivity_counts.values,
            names=sensitivity_counts.index,
            title="Data by Sensitivity Level",
            color_discrete_map={
                "Public": "#87CEEB",
                "Internal": "#FFD700",
                "Confidential": "#FF8C00",
                "Restricted": "#FF0000"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Sensitivity Details**")
        for sensitivity, count in sensitivity_counts.items():
            pct = round(100 * count / len(filtered_df), 1)
            st.write(f"• {sensitivity}: {count} datasets ({pct}%)")
    else:
        st.info("No sensitivity data available")

with tab_size:
    st.subheader("Dataset Size Analysis")
    
    if len(filtered_df) > 0 and "size_mb" in filtered_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            sorted_df = filtered_df.nlargest(10, "size_mb").reset_index(drop=True)
            fig = px.bar(
                sorted_df,
                x="size_mb",
                y="dataset_name",
                orientation="h",
                title="Top 10 Largest Datasets",
                labels={"size_mb": "Size (MB)", "dataset_name": "Dataset"},
                color="size_mb",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Size Statistics**")
            st.write(f"• Total: {filtered_df['size_mb'].sum()} MB")
            st.write(f"• Average: {filtered_df['size_mb'].mean():.0f} MB")
            st.write(f"• Median: {filtered_df['size_mb'].median():.0f} MB")
            st.write(f"• Min: {filtered_df['size_mb'].min()} MB")
            st.write(f"• Max: {filtered_df['size_mb'].max()} MB")
    else:
        st.info("No size data available")

with tab_access:
    st.subheader("Data Access Patterns (Last 7 Days)")
    
    if len(filtered_df) > 0 and "access_count_7d" in filtered_df.columns:
        # Most accessed datasets
        most_accessed = filtered_df.nlargest(10, "access_count_7d").reset_index(drop=True)
        
        fig = px.bar(
            most_accessed,
            x="dataset_name",
            y="access_count_7d",
            title="Most Accessed Datasets (7d)",
            labels={"dataset_name": "Dataset", "access_count_7d": "Access Count"},
            color="access_count_7d",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Access statistics
        st.write("**Access Statistics**")
        st.write(f"• Total Accesses: {filtered_df['access_count_7d'].sum():,}")
        st.write(f"• Average Accesses/Dataset: {filtered_df['access_count_7d'].mean():.0f}")
        st.write(f"• Most Accessed: {most_accessed.iloc[0]['dataset_name']} ({most_accessed.iloc[0]['access_count_7d']} times)")
    else:
        st.info("No access data available")

st.divider()

# ===== DETAILED METADATA TABLE =====
st.subheader(" Complete Metadata Catalog")

st.dataframe(filtered_df, use_container_width=True, height=400)

st.divider()

# ===== AI DATA INSIGHTS =====
st.subheader(" AI Data Insights")

if is_openai_configured():
    with st.expander(" Get AI Analysis of Dataset Patterns", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info("Ask AI about dataset patterns, relationships, and recommendations.")
        
        with col2:
            user_question = st.text_area(
                "Ask about dataset metadata:",
                placeholder="E.g., What patterns do you see in data quality? Which datasets need attention?",
                height=100,
                key="ai_metadata_question"
            )
            
            if st.button(" Analyze Patterns", type="primary", use_container_width=True):
                if user_question:
                    metadata_summary = f"""
                    Total Datasets: {len(filtered_df)}
                    Total Records: {filtered_df['record_count'].sum() if 'record_count' in filtered_df.columns else 0:,}
                    Total Size: {filtered_df['size_mb'].sum() if 'size_mb' in filtered_df.columns else 0} MB
                    
                    Quality Distribution:
                    {filtered_df['data_quality'].value_counts().to_string() if 'data_quality' in filtered_df.columns else 'N/A'}
                    
                    Sensitivity Distribution:
                    {filtered_df['sensitivity'].value_counts().to_string() if 'sensitivity' in filtered_df.columns else 'N/A'}
                    
                    User Question: {user_question}
                    """
                    
                    with st.spinner("Analyzing metadata..."):
                        success, response = explain_statistics(metadata_summary)
                        
                        if success:
                            st.success(" Analysis Complete")
                            st.write(response)
                        else:
                            st.error(f" Error: {response}")
                else:
                    st.warning("Please ask a question about the data.")
else:
    st.warning("""
     **AI Insights Not Available**
    
    To enable AI features, set the `OPENAI_API_KEY` environment variable.
    """)

st.divider()

# Data Governance Info
with st.expander(" Data Governance & Best Practices", expanded=False):
    st.markdown("""
    ### Data Governance Framework
    
    #### Data Classification
    - **Public**: No sensitivity restrictions
    - **Internal**: Employee access only
    - **Confidential**: Department/authorized users
    - **Restricted**: Executive/security clearance only
    
    #### Data Quality Levels
    - **Excellent**: ≥99% accuracy, complete, validated
    - **Good**: 95-99% accuracy, mostly complete
    - **Fair**: 80-95% accuracy, some gaps
    - **Poor**: <80% accuracy, significant issues
    
    #### Best Practices
    1. Regular data quality audits
    2. Access control enforcement
    3. Data lifecycle management
    4. Documentation and metadata maintenance
    5. Incident response procedures
    6. Backup and recovery testing
    """)

st.divider()

# Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Incidents", use_container_width=True):
        st.switch_page("pages/Incidents.py")

with col2:
    if st.button(" Users", use_container_width=True):
        st.switch_page("pages/Users.py")

with col3:
    if st.button(" Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")

with col4:
    if st.button(" Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

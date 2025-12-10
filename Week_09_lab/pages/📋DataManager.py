"""CRUD Demo: IT Tickets Data Manager.

This page demonstrates Create, Read, Update, Delete operations on IT ticket data.
Data is loaded from Week_08_Lab/DATA/it_tickets.csv for demo purposes.
"""

import streamlit as st
import pandas as pd
from session_state import init_session
from pathlib import Path

st.set_page_config(page_title="Data Manager", page_icon="📊", layout="wide")

init_session()

st.title("📊 IT Tickets Data Manager")

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    st.info("Please log in from the home page.")
    st.stop()

st.success(f"Logged in as: **{st.session_state.username}**")

# Path to demo data
data_path = Path(__file__).parent.parent / "DATA" / "it_tickets.csv"

if not data_path.exists():
    st.warning(f"Demo data not found at {data_path}")
    st.info("Creating sample data for demo...")
    # Create sample data if file doesn't exist
    sample_data = {
        "ticket_id": ["TCK-1001", "TCK-1002", "TCK-1003", "TCK-1004", "TCK-1005"],
        "title": ["Network Down", "Password Reset", "Email Issue", "Printer Error", "Software Update"],
        "priority": ["High", "Medium", "Medium", "Low", "High"],
        "status": ["Open", "Closed", "In Progress", "Open", "Closed"],
        "assignee": ["Siele", "bob", "charlie", "Griffins", "bob"],
        "created_date": ["2025-11-01", "2025-11-02", "2025-11-03", "2025-11-04", "2025-11-05"],
    }
    df = pd.DataFrame(sample_data)
else:
    df = pd.read_csv(data_path)
    # ticket_id is already a string in TCK-#### format, keep it as is

# Initialize session state for CRUD operations
if "tickets_data" not in st.session_state:
    st.session_state.tickets_data = df.copy()
else:
    # Ensure consistent data types in session state
    st.session_state.tickets_data = st.session_state.tickets_data.astype(df.dtypes)

# Tabs for CRUD operations
tab_read, tab_create, tab_update, tab_delete = st.tabs(["📖 Read", "➕ Create", "✏️ Update", "❌ Delete"])

# ===== READ TAB =====
with tab_read:
    st.subheader("View All Tickets")
    st.dataframe(st.session_state.tickets_data, use_container_width=True)
    
    # Filter by status and priority
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Filter by Status")
        statuses = st.session_state.tickets_data["status"].unique().tolist()
        selected_status = st.selectbox("Select Status:", ["All"] + sorted(statuses))
    
    with col2:
        st.subheader("Filter by Priority")
        selected_priority = st.selectbox("Select Priority:", ["All", "High", "Medium", "Low"])
    
    # Apply filters
    filtered_df = st.session_state.tickets_data.copy()
    
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]
    
    if selected_priority != "All":
        filtered_df = filtered_df[filtered_df["priority"] == selected_priority]
    
    st.dataframe(filtered_df, use_container_width=True)
    st.info(f"Found {len(filtered_df)} tickets matching filters")
    
    st.metric(label="Total Tickets", value=len(st.session_state.tickets_data))


# ===== CREATE TAB =====
with tab_create:
    st.subheader("Create New Ticket")
    
    with st.form("create_ticket_form"):
        new_title = st.text_input("Title")
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        new_status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        new_assignee = st.text_input("Assignee")
        
        if st.form_submit_button("Create Ticket"):
            if not new_title or not new_assignee:
                st.error("Please fill in all fields.")
            else:
                # Get next ticket ID by extracting number from TCK-#### and incrementing
                last_id_str = st.session_state.tickets_data["ticket_id"].iloc[-1]
                last_num = int(last_id_str.split("-")[-1])  # Extract number from "TCK-1005"
                next_num = last_num + 1
                next_id = f"TCK-{next_num:04d}"
                
                from datetime import date
                new_ticket = {
                    "ticket_id": next_id,
                    "title": new_title,
                    "priority": new_priority,
                    "status": new_status,
                    "assignee": new_assignee,
                    "created_date": str(date.today()),
                }
                
                st.session_state.tickets_data = pd.concat(
                    [st.session_state.tickets_data, pd.DataFrame([new_ticket])],
                    ignore_index=True
                )
                st.success(f"✅ Ticket {next_id} created successfully!")
                st.balloons()


# ===== UPDATE TAB =====
with tab_update:
    st.subheader("Update Ticket")
    
    if len(st.session_state.tickets_data) == 0:
        st.warning("No tickets available to update.")
    else:
        # Select ticket to update
        ticket_ids = st.session_state.tickets_data["ticket_id"].tolist()
        selected_ticket_id = st.selectbox("Select Ticket ID to Update:", ticket_ids, key="update_ticket_id")
        
        # Get the ticket data
        ticket_idx = st.session_state.tickets_data[st.session_state.tickets_data["ticket_id"] == selected_ticket_id].index[0]
        ticket = st.session_state.tickets_data.loc[ticket_idx]
        
        with st.form("update_ticket_form"):
            updated_title = st.text_input("Title", value=ticket["title"])
            updated_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(ticket["priority"]))
            updated_status = st.selectbox("Status", ["Open", "In Progress", "Closed"], index=["Open", "In Progress", "Closed"].index(ticket["status"]))
            updated_assignee = st.text_input("Assignee", value=ticket["assignee"])
            
            if st.form_submit_button("Save Changes"):
                st.session_state.tickets_data.loc[ticket_idx, "title"] = updated_title
                st.session_state.tickets_data.loc[ticket_idx, "priority"] = updated_priority
                st.session_state.tickets_data.loc[ticket_idx, "status"] = updated_status
                st.session_state.tickets_data.loc[ticket_idx, "assignee"] = updated_assignee
                
                st.success(f"✅ Ticket {selected_ticket_id} updated successfully!")


# ===== DELETE TAB =====
with tab_delete:
    st.subheader("Delete Ticket")
    
    if len(st.session_state.tickets_data) == 0:
        st.warning("No tickets available to delete.")
    else:
        ticket_ids = st.session_state.tickets_data["ticket_id"].tolist()
        selected_delete_id = st.selectbox("Select Ticket ID to Delete:", ticket_ids, key="delete_ticket_id")
        
        ticket_to_delete = st.session_state.tickets_data[st.session_state.tickets_data["ticket_id"] == selected_delete_id].iloc[0]
        st.info(f"**Ticket #{selected_delete_id}**: {ticket_to_delete['title']}")
        
        if st.button("⚠️ Confirm Delete", type="secondary"):
            st.session_state.tickets_data = st.session_state.tickets_data[
                st.session_state.tickets_data["ticket_id"] != selected_delete_id
            ]
            st.success(f"✅ Ticket #{selected_delete_id} deleted successfully!")
            st.rerun()

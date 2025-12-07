"""Data Manager: CRUD operations for IT Tickets."""
import streamlit as st
import pandas as pd
from pathlib import Path
from session_state import init_session

st.set_page_config(
    page_title="Data Manager",
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

st.title(" IT Tickets Data Manager")
st.success(f"Logged in as: **{st.session_state.username}**")

# Path to data
data_path = Path(__file__).parent.parent / "DATA" / "it_tickets.csv"

# Initialize or load data
if not data_path.exists():
    st.warning("📁 No existing data. Creating sample tickets...")
    sample_data = {
        "ticket_id": ["TCK-1001", "TCK-1002", "TCK-1003", "TCK-1004", "TCK-1005"],
        "title": ["Network Down", "Password Reset", "Email Issue", "Printer Error", "Software Update"],
        "priority": ["High", "Medium", "Medium", "Low", "High"],
        "status": ["Open", "Closed", "In Progress", "Open", "Closed"],
        "assignee": ["Griffins", "Siele", "Alice", "Diana", "Bob"],
        "created_date": ["2025-11-01", "2025-11-02", "2025-11-03", "2025-11-04", "2025-11-05"],
    }
    df = pd.DataFrame(sample_data)
else:
    df = pd.read_csv(data_path)

# Initialize session state for CRUD
if "tickets_data" not in st.session_state:
    st.session_state.tickets_data = df.copy()

st.divider()

# ===== TABS FOR CRUD OPERATIONS =====
tab_read, tab_create, tab_update, tab_delete = st.tabs(["📖 Read", " Create", " Update", " Delete"])

# ===== READ TAB =====
with tab_read:
    st.subheader("View All Tickets")
    
    # Display all tickets
    st.dataframe(st.session_state.tickets_data, use_container_width=True, height=300)
    
    st.info(f"Total: {len(st.session_state.tickets_data)} tickets")
    
    st.divider()
    st.subheader("Advanced Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        statuses = st.session_state.tickets_data["status"].unique().tolist()
        selected_status = st.selectbox("Filter by Status:", ["All"] + sorted(statuses), key="filter_status")
    
    with col2:
        priorities = st.session_state.tickets_data["priority"].unique().tolist()
        selected_priority = st.selectbox("Filter by Priority:", ["All", "High", "Medium", "Low"], key="filter_priority")
    
    with col3:
        assignees = st.session_state.tickets_data["assignee"].unique().tolist()
        selected_assignee = st.selectbox("Filter by Assignee:", ["All"] + sorted(assignees), key="filter_assignee")
    
    # Apply filters
    filtered_df = st.session_state.tickets_data.copy()
    
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]
    if selected_priority != "All":
        filtered_df = filtered_df[filtered_df["priority"] == selected_priority]
    if selected_assignee != "All":
        filtered_df = filtered_df[filtered_df["assignee"] == selected_assignee]
    
    st.write(f"**Filtered Results: {len(filtered_df)} tickets**")
    st.dataframe(filtered_df, use_container_width=True, height=300)
    
    # Export options
    col_csv, col_json = st.columns(2)
    
    with col_csv:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label=" Download CSV",
            data=csv,
            file_name="tickets.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_json:
        json = filtered_df.to_json(orient="records", indent=2)
        st.download_button(
            label=" Download JSON",
            data=json,
            file_name="tickets.json",
            mime="application/json",
            use_container_width=True
        )

# ===== CREATE TAB =====
with tab_create:
    st.subheader("Create New Ticket")
    
    with st.form("create_ticket_form", clear_on_submit=True):
        new_title = st.text_input("Ticket Title", placeholder="E.g., Network connectivity issue")
        new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        new_status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        new_assignee = st.text_input("Assigned To", placeholder="Enter assignee name")
        
        submitted_create = st.form_submit_button(" Create Ticket", type="primary", use_container_width=True)
        
        if submitted_create:
            if not new_title or not new_assignee:
                st.error(" Please fill in all fields.")
            else:
                # Generate new ticket ID
                existing_ids = st.session_state.tickets_data["ticket_id"].tolist()
                last_id = max([int(tid.split("-")[1]) for tid in existing_ids if "-" in tid])
                new_id = f"TCK-{last_id + 1}"
                
                # Create new ticket
                new_ticket = pd.DataFrame({
                    "ticket_id": [new_id],
                    "title": [new_title],
                    "priority": [new_priority],
                    "status": [new_status],
                    "assignee": [new_assignee],
                    "created_date": [pd.Timestamp.now().strftime("%Y-%m-%d")]
                })
                
                st.session_state.tickets_data = pd.concat(
                    [st.session_state.tickets_data, new_ticket],
                    ignore_index=True
                )
                
                # Save to CSV
                st.session_state.tickets_data.to_csv(data_path, index=False)
                
                st.success(f" Ticket {new_id} created successfully!")
                st.balloons()

# ===== UPDATE TAB =====
with tab_update:
    st.subheader("Update Existing Ticket")
    
    if len(st.session_state.tickets_data) == 0:
        st.info("No tickets to update.")
    else:
        # Select ticket to update
        ticket_to_update = st.selectbox(
            "Select ticket to update:",
            st.session_state.tickets_data["ticket_id"].tolist(),
            key="update_ticket_select"
        )
        
        # Get current ticket data
        current_ticket = st.session_state.tickets_data[
            st.session_state.tickets_data["ticket_id"] == ticket_to_update
        ].iloc[0]
        
        st.info(f"**Current Ticket:** {current_ticket['title']}")
        
        with st.form("update_ticket_form"):
            updated_title = st.text_input("Title", value=current_ticket["title"])
            updated_priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"],
                index=["Low", "Medium", "High"].index(current_ticket["priority"])
            )
            updated_status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Closed"],
                index=["Open", "In Progress", "Closed"].index(current_ticket["status"])
            )
            updated_assignee = st.text_input("Assigned To", value=current_ticket["assignee"])
            
            submitted_update = st.form_submit_button(" Update Ticket", type="primary", use_container_width=True)
        
        if submitted_update:
            # Update the ticket
            idx = st.session_state.tickets_data[
                st.session_state.tickets_data["ticket_id"] == ticket_to_update
            ].index[0]
            
            st.session_state.tickets_data.loc[idx, "title"] = updated_title
            st.session_state.tickets_data.loc[idx, "priority"] = updated_priority
            st.session_state.tickets_data.loc[idx, "status"] = updated_status
            st.session_state.tickets_data.loc[idx, "assignee"] = updated_assignee
            
            # Save to CSV
            st.session_state.tickets_data.to_csv(data_path, index=False)
            
            st.success(f" Ticket {ticket_to_update} updated successfully!")

# ===== DELETE TAB =====
with tab_delete:
    st.subheader("Delete Ticket")
    st.warning(" This action cannot be undone!")
    
    if len(st.session_state.tickets_data) == 0:
        st.info("No tickets to delete.")
    else:
        ticket_to_delete = st.selectbox(
            "Select ticket to delete:",
            st.session_state.tickets_data["ticket_id"].tolist(),
            key="delete_ticket_select"
        )
        
        # Show ticket details
        ticket_info = st.session_state.tickets_data[
            st.session_state.tickets_data["ticket_id"] == ticket_to_delete
        ].iloc[0]
        
        st.info(f"**Will delete:** {ticket_info['title']} (Status: {ticket_info['status']})")
        
        col_confirm, col_cancel = st.columns(2)
        
        with col_confirm:
            if st.button(" Confirm Delete", type="primary", use_container_width=True):
                st.session_state.tickets_data = st.session_state.tickets_data[
                    st.session_state.tickets_data["ticket_id"] != ticket_to_delete
                ]
                
                # Save to CSV
                st.session_state.tickets_data.to_csv(data_path, index=False)
                
                st.success(f" Ticket {ticket_to_delete} deleted successfully!")
        
        with col_cancel:
            if st.button(" Cancel", use_container_width=True):
                st.info("Deletion cancelled.")

st.divider()

# Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")

with col2:
    if st.button(" Incidents", use_container_width=True):
        st.switch_page("pages/Incidents.py")

with col3:
    if st.button(" Users", use_container_width=True):
        st.switch_page("pages/Users.py")

with col4:
    if st.button(" Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")

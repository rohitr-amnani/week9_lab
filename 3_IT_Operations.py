import streamlit as st
import pandas as pd
import datetime
from app.data.tickets import get_all_tickets, insert_ticket, update_ticket_status, delete_ticket

st.set_page_config(page_title="IT Operations", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("IT Operations Dashboard")

# FETCH DATA 
df_tickets = get_all_tickets()


st.subheader("Ticket Metrics")

if not df_tickets.empty:
    # 1. Metrics
    total = len(df_tickets)
    high = len(df_tickets[df_tickets['priority'] == 'High'])
    open_t = len(df_tickets[df_tickets['status'] == 'Open'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total)
    col2.metric("High Priority", high)
    col3.metric("Open Tickets", open_t)

    # 2. Single Chart: Status Distribution
    st.subheader("Current Ticket Status")
    status_counts = df_tickets['status'].value_counts()
    st.bar_chart(status_counts)

else:
    st.info("No tickets found.")

#CRUD Operations
st.divider()
st.header("Ticket Management")

tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "View Queue", "Create Ticket", "Update Status", "Delete"
])

# --- READ ---
with tab_view:
    st.dataframe(df_tickets, use_container_width=True)

# --- CREATE ---
with tab_add:
    with st.form("add_tick"):
        tid = st.text_input("Ticket ID (e.g. T-100)")
        subj = st.text_input("Subject")
        prio = st.selectbox("Priority", ["Low", "Medium", "High"])
        cat = st.selectbox("Category", ["Hardware", "Software", "Network"])
        desc = st.text_area("Description")
        
        if st.form_submit_button("Submit"):
            today = str(datetime.date.today())
            insert_ticket(tid, prio, "Open", cat, subj, desc, today, None, None)
            st.success("Created!")
            st.rerun()

# --- UPDATE ---
with tab_update:
    if not df_tickets.empty:
        opts = {f"{row['ticket_id']} (ID: {row['id']})": row['id'] for i, row in df_tickets.iterrows()}
        sel_lbl = st.selectbox("Select Ticket", list(opts.keys()))
        sel_id = opts[sel_lbl]
        new_stat = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
        
        if st.button("Update Status"):
            update_ticket_status(sel_id, new_stat)
            st.success("Updated!")
            st.rerun()

# --- DELETE ---
with tab_delete:
    if not df_tickets.empty:
        ids = df_tickets['id'].tolist()
        del_id = st.selectbox("Select ID to Delete", ids)
        if st.button("Confirm Delete", type="primary"):
            delete_ticket(del_id)
            st.success("Deleted.")
            st.rerun()
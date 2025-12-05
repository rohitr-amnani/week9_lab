import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident

st.set_page_config(page_title="Cybersecurity", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("Cybersecurity Dashboard")

# --- FETCH DATA ---
df_incidents = get_all_incidents()

#
st.subheader("Security Metrics")

if not df_incidents.empty:
    # 1. Metrics
    total = len(df_incidents)
    critical = len(df_incidents[df_incidents['severity'] == 'Critical'])
    open_cases = len(df_incidents[df_incidents['status'] == 'Open'])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidents", total)
    col2.metric("Critical Threats", critical)
    col3.metric("Open Cases", open_cases)

    # 2. Single Chart: Threat Distribution
    st.subheader("Threat Distribution by Type")
    type_counts = df_incidents['incident_type'].value_counts()
    st.bar_chart(type_counts)

else:
    st.info("No data available.")


st.divider()
st.header(" Incident Management")

tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "View Data", "Add Incident", "Update Status", "Delete"
])

# --- READ ---
with tab_view:
    st.dataframe(df_incidents, use_container_width=True)

# --- CREATE ---
with tab_add:
    with st.form("add_inc"):
        date = st.date_input("Date")
        inc_type = st.selectbox("Type", ["Malware", "Phishing", "DDoS", "Intrusion", "Ransomware", "SQL Injection"])
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "Closed", "Investigating"])
        desc = st.text_area("Description")
        
        if st.form_submit_button("Submit Report"):
            insert_incident(str(date), inc_type, severity, status, desc, st.session_state.username)
            st.success("Added!")
            st.rerun()

# --- UPDATE ---
with tab_update:
    if not df_incidents.empty:
        opts = {f"ID {row['id']} ({row['incident_type']})": row['id'] for i, row in df_incidents.iterrows()}
        sel_lbl = st.selectbox("Select Incident", list(opts.keys()))
        sel_id = opts[sel_lbl]
        new_stat = st.selectbox("New Status", ["Open", "Closed", "Investigating", "Resolved"])
        
        if st.button("Update Status"):
            update_incident_status(sel_id, new_stat)
            st.success("Updated!")
            st.rerun()

# --- DELETE ---
with tab_delete:
    if not df_incidents.empty:
        ids = df_incidents['id'].tolist()
        del_id = st.selectbox("Select ID to Delete", ids)
        if st.button("Confirm Delete", type="primary"):
            delete_incident(del_id)
            st.success("Deleted.")
            st.rerun()
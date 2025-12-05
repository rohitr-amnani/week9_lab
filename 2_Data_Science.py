import streamlit as st
import pandas as pd
import datetime
from app.data.datasets import get_all_datasets, insert_dataset, update_dataset_record_count, delete_dataset

st.set_page_config(page_title="Data Science", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

st.title("Data Science Dashboard")

# --- FETCH DATA ---
df_datasets = get_all_datasets()


st.subheader("Dataset Metrics")

if not df_datasets.empty:
    # 1. Metrics
    total_files = len(df_datasets)
    total_records = df_datasets['record_count'].sum()
    total_size = (df_datasets['file_size_mb'].sum() / 1024)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Datasets", total_files)
    col2.metric("Total Records", f"{total_records:,}")
    col3.metric("Total Storage (GB)", f"{total_size:.2f}")

    # 2. Single Chart: Categories
    st.subheader("Datasets by Category")
    cat_counts = df_datasets['category'].value_counts()
    st.bar_chart(cat_counts)

else:
    st.info("No datasets registered.")


st.divider()
st.header("Dataset Management")

tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "View Data", "Register Dataset", "Update Count", "Delete"
])

# --- READ ---
with tab_view:
    st.dataframe(df_datasets, use_container_width=True)

# --- CREATE ---
with tab_add:
    with st.form("add_ds"):
        name = st.text_input("Dataset Name")
        cat = st.selectbox("Category", ["Finance", "Health", "Sales", "Operations", "Security"])
        src = st.text_input("Source URL")
        cnt = st.number_input("Count", min_value=0)
        size = st.number_input("Size (MB)", min_value=0.0)
        
        if st.form_submit_button("Register"):
            today = str(datetime.date.today())
            insert_dataset(name, cat, src, today, cnt, size)
            st.success("Registered!")
            st.rerun()

# --- UPDATE ---
with tab_update:
    if not df_datasets.empty:
        opts = {f"{row['dataset_name']} (ID: {row['id']})": row['id'] for i, row in df_datasets.iterrows()}
        sel_lbl = st.selectbox("Select Dataset", list(opts.keys()))
        sel_id = opts[sel_lbl]
        new_cnt = st.number_input("New Record Count", min_value=0)
        
        if st.button("Update Count"):
            update_dataset_record_count(sel_id, new_cnt)
            st.success("Updated!")
            st.rerun()

# --- DELETE ---
with tab_delete:
    if not df_datasets.empty:
        ids = df_datasets['id'].tolist()
        del_id = st.selectbox("Select ID to Delete", ids)
        if st.button("Confirm Delete", type="primary"):
            delete_dataset(del_id)
            st.success("Deleted.")
            st.rerun()
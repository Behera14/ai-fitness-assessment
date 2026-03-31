import streamlit as st
import pandas as pd
import os

st.title("💰 Transaction Reconciliation Dashboard")

# Load file
base_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_path, "final_output.csv")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    st.subheader("📊 Reconciliation Report")
    st.dataframe(df)

    st.subheader("📈 Issue Summary")
    st.write(df["issue"].value_counts())

    # Filter option
    issue_filter = st.selectbox("Filter by Issue", ["All"] + list(df["issue"].unique()))

    if issue_filter != "All":
        filtered_df = df[df["issue"] == issue_filter]
        st.dataframe(filtered_df)

else:
    st.error("❌ Please run reconciliation script first to generate output file")
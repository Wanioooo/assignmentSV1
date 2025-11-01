# main.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def run_homepage():
    st.title("🎓 Academic Performance Analysis Dashboard")
    st.markdown("Welcome to the academic performance dashboard!")

    # Load data (reuse your current load_data function)
    URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"

    @st.cache_data
    def load_data():
        df = pd.read_csv(URL)
        return df

    df = load_data()

    st.sidebar.header("Data Source & Overview")
    st.sidebar.markdown(f"Data Loaded Successfully: **{len(df)} records**")

    if st.sidebar.checkbox("Show Raw Data", False):
        st.subheader("Raw Data Sample")
        st.dataframe(df.head())

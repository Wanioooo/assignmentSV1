import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load the academic performance dataset from GitHub."""
    URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
    df = pd.read_csv(URL)
    return df


def split_multi_select(df, column_name):
    """Splits a multi-select column and counts each option frequency."""
    reasons_df = df[column_name].str.get_dummies(sep=';')
    counts = reasons_df.sum().sort_values(ascending=False)
    return counts

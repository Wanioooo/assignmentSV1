import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    """Load the academic performance dataset from GitHub."""
    URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
    try:
        df = pd.read_csv(URL)
    except:
        st.warning("⚠️ Could not load the actual CSV file. Displaying dummy data for structure review.")
        df = pd.DataFrame({
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'Study Time (hrs)': np.random.randint(1, 15, 100),
            'Final Grade (0-20)': np.random.randint(5, 20, 100)
        })
    return df

def run_objective1():
    st.title("Objective 1: Data Distribution and Exploration")
    st.write("This page focuses on understanding the raw distribution of key variables in the dataset.")

    df = load_data()

    st.subheader("Raw Data Sample")
    st.dataframe(df.head())

    st.subheader("Grade Distribution by Gender")
    fig = px.bar(df.groupby('Gender')['Final Grade (0-20)'].mean().reset_index(),
                 x='Gender', y='Final Grade (0-20)',
                 title='Average Grade by Gender',
                 color='Gender',
                 color_discrete_map={'Male': 'blue', 'Female': 'red'})
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    run_objective1()

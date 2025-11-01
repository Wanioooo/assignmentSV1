import streamlit as st
import pandas as pd
import numpy as np

# A function to simulate data loading (replace with actual loading from your CSV)
@st.cache_data
def load_data(filepath):
    # In a real app, you would use: return pd.read_csv(filepath)
    # Using dummy data for demonstration
    data = pd.DataFrame({
        'Gender': np.random.choice(['Male', 'Female'], 100),
        'Study Time (hrs)': np.random.randint(1, 15, 100),
        'Final Grade (0-20)': np.random.randint(5, 20, 100)
    })
    return data

# The main function for this specific page
def run_objective1():
    st.title("Objective 1: Data Distribution and Exploration")
    st.write("This page focuses on understanding the raw distribution of key variables in the dataset.")

    # Load the data
    try:
        # NOTE: Adjust the path if your structure changes
        df = load_data('../new_dataset_academic_performance (1).csv')
    except:
        st.warning("⚠️ Could not load the actual CSV file. Displaying dummy data for structure review.")
        df = load_data(None) # Use dummy data if loading fails

    st.subheader("Raw Data Sample")
    st.dataframe(df.head())

    # Example visualization for this objective
    st.subheader("Grade Distribution by Gender")
    fig = st.bar_chart(df.groupby('Gender')['Final Grade (0-20)'].mean().reset_index(), x='Gender', y='Final Grade (0-20)')


# The entry point for the page file
if __name__ == "__main__":
    run_objective1()

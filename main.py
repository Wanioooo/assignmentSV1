import streamlit as st

# Set up the main page configuration (optional but recommended)
st.set_page_config(
    page_title="Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide" # Use 'wide' layout for more space
)

# --- Content for the Main Page (Home) ---
st.title("🎓 Project Home: Academic Performance Analysis")
st.markdown("""
Welcome to the Academic Performance Dashboard. 
This application is organized into three main objectives, accessible via the sidebar navigation.

This `main.py` file serves as the default entry page.
It is highly recommended to run your app using this command:
`streamlit run main.py`

### Project Overview
Use the navigation on the left to explore:
- **Objective 1:** Detailed Data Exploration and Cleaning.
- **Objective 2:** Correlation Analysis and Feature Engineering.
- **Objective 3:** Predictive Modeling and Insights.
""")

st.info("👈 Select an Objective from the sidebar to navigate to a different page.")

# You can display basic content or a project summary here.
if st.button("Load Quick Data Preview"):
    # Note: In a real app, you would load your data here (e.g., from new_dataset_academic_performance (1).csv)
    st.subheader("Example Data Snippet")
    st.dataframe({
        'Student ID': [101, 102, 103],
        'Gender': ['F', 'M', 'F'],
        'Math Score': [90, 75, 88],
        'Reading Score': [85, 80, 92]
    })

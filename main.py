import streamlit as st

# --- Configuration ---
st.set_page_config(
    page_title="Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

def main_page():
    """Defines the content for the application's main/home page."""
    st.title("🎓 Academic Performance Analysis Dashboard")
    st.markdown("""
        Welcome to the Academic Performance Dashboard. This application allows you
        to explore different objectives related to student data.

        **To get started, select one of the analysis objectives from the sidebar:**

        * **Objective 1:** Explore Data Distribution
        * **Objective 2:** Predict Student Outcomes
        * **Objective 3:** Compare Group Performance

        This data exploration uses the `new_dataset_academic_performance.csv` file.
    """)

    # Optional: Display a small section on the main page
    st.header("Quick Overview")
    st.info("The individual analysis pages are located in the `pages/` directory.")

if __name__ == "__main__":
    main_page()

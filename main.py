import streamlit as st

# This function controls the browser tab title and the default layout
st.set_page_config(
    page_title="Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Content placed in the Sidebar (Navigation Bar) ---
# The links to the pages will appear AUTOMATICALLY above this custom content.
st.sidebar.title("📚 Project Navigation")
st.sidebar.markdown(
    """
    Select one of the objectives above to view the analysis 
    and interactive data tools for that objective.
    """
)
st.sidebar.write("---")
st.sidebar.subheader("App Info")
st.sidebar.markdown("App Version 1.0. Developed for Academic Analysis.")


# --- Content for the Home Page ---
st.title("🎓 Welcome to the Academic Performance Dashboard")
st.header("Project Overview")

st.markdown("""
Welcome! This application is designed to help you analyze and visualize 
the key factors affecting academic performance using the provided dataset.

Your navigation is automatically handled by Streamlit. All you need to do 
is put your Python files in the `pages/` folder, and they appear as links 
in the sidebar (on the left) right away!

### How to use the app:
1.  **Select** a link in the **"Project Navigation"** sidebar.
2.  Each link corresponds to a specific objective (`objective1.py`, etc.).
3.  Each page contains the necessary code and visuals for that analysis step.

👉 **Start by selecting '1. Data Exploration' to begin the analysis.**
""")

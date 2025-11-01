# pages.py
import streamlit as st
from pages import objective1, objective2, objective3  # Import your page modules
import main  # Import homepage content

# Set page config
st.set_page_config(
    page_title="Academic Performance Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation menu
page_selection = st.sidebar.radio(
    "📊 Select Page",
    (
        "Homepage",
        "Objective 1: Demographics",
        "Objective 2: Learning Factors",
        "Objective 3: Placeholder"
    )
)

# Render the selected page
if page_selection == "Homepage":
    main.run_homepage()  # We’ll create a small function in main.py for homepage
elif page_selection == "Objective 1: Demographics":
    objective1.run_objective1()
elif page_selection == "Objective 2: Learning Factors":
    objective2.run_objective2()
elif page_selection == "Objective 3: Placeholder":
    objective3.run_objective3()  # Placeholder function for future page

import streamlit as st

# Set the page title and layout
st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide"
)

# Homepage content
st.title("🎓 Academic Performance Dashboard")
st.markdown("""
Welcome to the Academic Performance Dashboard!  

Use the **sidebar** to navigate between different objectives:
- Objective 1: Core Demographics  
- Objective 2: Learning Factors  
- Objective 3: Advanced Trends  

Each page contains interactive visualizations for analysis.
""")

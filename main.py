# main.py
import streamlit as st

st.set_page_config(
    page_title="Academic Performance Analysis",
    layout="wide",
)
# This content is what you see when the app first loads.
st.title("🏠 Homepage") 
st.write("Use the sidebar to navigate to Objective 1 or Objective 2.")

# --- NO st.Page(), st.navigation(), or pg.run() HERE ---

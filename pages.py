import streamlit as st
import main
from pages import objective1, objective2, objective3

st.set_page_config(page_title="Academic Performance Dashboard", layout="wide")

page = st.sidebar.radio(
    "📊 Select Page",
    ["Homepage", "Objective 1", "Objective 2", "Objective 3"]
)

if page == "Homepage":
    main.run_homepage()
elif page == "Objective 1":
    objective1.run_objective1()
elif page == "Objective 2":
    objective2.run_objective2()
elif page == "Objective 3":
    objective3.run_objective3()

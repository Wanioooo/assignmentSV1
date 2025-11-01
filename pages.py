# pages.py
import streamlit as st

st.set_page_config(
    page_title="Academic Performance Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

home = st.Page('main.py', title='Homepage', default=True, icon=":material/home:")
page1 = st.Page('pages/objective1.py', title='Objective 1: Demographics', icon=":material/bar_chart:")
page2 = st.Page('pages/objective2.py', title='Objective 2: Learning Factors', icon=":material/assignment_turned_in:")
page3 = st.Page('pages/objective3.py', title='Objective 3: Under Development', icon=":material/lab_profile:")

pg = st.navigation({
    "Main Menu": [home, page1, page2, page3]
})

pg.run()

import streamlit as st

st.set_page_config(
    page_title="Academic Performance Analysis"
)

page1 = st.Page('pages/objective1.py', title='Kesan Dalam Pembelajaran', icon=":material/assignment_turned_in:")
page2 = st.Page('pages/objective2.py', title='Kesan Dalam Pembelajaran', icon=":material/assignment_turned_in:")
home = st.Page('main.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [page1, page2]
        }
    )

pg.run()

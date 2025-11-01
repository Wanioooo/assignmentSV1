import streamlit as st

st.set_page_config(
    page_title="Academic Performance Analysis"
)

page1 = st.Page('main.py', title='Socio-economic and Demographic Influence', icon=":material/thumb_up_off_alt:")

page2 = st.Page('objective2.py', title='Kesan Dalam Pembelajaran', icon=":material/assignment_turned_in:")

pg = st.navigation(
        {
            "Menu": [page1, page2]
        }
    )

pg.run()

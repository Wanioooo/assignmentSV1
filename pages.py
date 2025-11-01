import streamlit as st

st.set_page_config(
    page_title="Online Learning Survey"
)

page1 = st.Page('main.py', title='Kepuasan Pelajar Dalam Pembelajaran', icon=":material/thumb_up_off_alt:")

page2 = st.Page('objective1.py', title='Kesan Dalam Pembelajaran', icon=":material/assignment_turned_in:")

home = st.Page('Homepage.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, page1, page2]
        }
    )

pg.run()

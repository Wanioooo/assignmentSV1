st.set_page_config(
    page_title="Academic Performance Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the pages using the functions created above
page1 = st.Page(objective1_page, title='Objective 1: Demographics', icon=":material/bar_chart:")
page2 = st.Page(objective2_page, title='Objective 2: Learning Factors', icon=":material/assignment_turned_in:")
home = st.Page(home_page, title='Homepage', default=True, icon=":material/home:")

# Create the navigation menu
pg = st.navigation(
    {
        "Menu": [home, page1, page2] # Corrected the typo (home instead of hone)
    }
)

# Run the navigation (This is the final command needed for this approach)
pg.run()

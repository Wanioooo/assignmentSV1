import streamlit as st
import plotly.express as px
from data_loader import setup_page # Import the common setup function

# --- Visualization Functions (Objective 1) ---

# 1. Box Plot: Current CGPA vs. Gender
def plot_cgpa_vs_gender(data):
    fig = px.box(data, x='Gender', y='Current_CGPA', title='CGPA Distribution by Gender', color='Gender', color_discrete_map={'Male': 'blue', 'Female': 'red'}, height=450, range_y=[2.0, 4.0])
    fig.update_layout(xaxis_title='Gender', yaxis_title='Current CGPA')
    return fig

# 2. Heatmap: Average Current CGPA by Admission Year and Age Group
def plot_cgpa_heatmap(data):
    heatmap_data = data.groupby(['Admission_Year', 'Age_Group'])['Current_CGPA'].mean().unstack()
    age_order = ['18-20', '21-22', '23-24', '25+']
    heatmap_data = heatmap_data.reindex(columns=age_order)
    fig = px.imshow(heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index.astype(str), color_continuous_scale="YlGnBu", aspect="auto", text_auto=".2f", title='Average CGPA by Admission Year and Age Group')
    fig.update_layout(xaxis_title='Age Group (Years)', yaxis_title='University Admission Year', height=500)
    fig.update_coloraxes(colorbar_title='Average Current CGPA')
    return fig

# 3. Grouped Bar Plot: Average CGPA by Income Group and Meritorious Scholarship Status
def plot_cgpa_by_income_scholarship(data):
    grouped_data = data.groupby(['Income_Group', 'Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(grouped_data, x='Income_Group', y='Current_CGPA', color='Meritorious_Scholarship', barmode='group', title='Average CGPA by Family Income Group and Meritorious Scholarship Status', labels={'Current_CGPA': 'Average Current CGPA', 'Meritorious_Scholarship': 'Meritorious Scholarship?'}, height=500, color_discrete_map={'Yes': 'green', 'No': 'red'})
    fig.update_layout(xaxis_title='Family Income Group', yaxis_title='Average Current CGPA')
    return fig

# --- Main Streamlit App for Objective 1 ---

df = setup_page("Objective 1: Core Performance")

st.title("🎯 Objective 1: Core Performance Metrics & Demographics")
st.markdown("Analyzing CGPA distribution by key demographic factors.")

st.subheader("Summary Box: Core Performance")
with st.container(border=True):
    st.markdown("""
    **Summary (100-150 words):**
    This objective explores the relationship between **Current CGPA** and key factors like **Gender**, **Admission Year/Age**, and **Family Income/Scholarship status**. The visualizations reveal that CGPA distributions are largely similar across genders, though potential differences in median CGPA may exist. The heatmap indicates that older students (25+) often maintain slightly lower average CGPAs, particularly those admitted in later years (2020-2021). Notably, students receiving a **Meritorious Scholarship** consistently achieve a higher average CGPA across all income groups, with the difference being most pronounced in the Low-Income bracket, suggesting the scholarship is a strong positive indicator of academic success regardless of financial background.
    """)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)
with col2:
    st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)

st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)

st.subheader("Interpretation/Discussion: Core Performance")
st.markdown("""
* **CGPA vs. Gender:** The box plot shows that both male and female CGPA distributions are concentrated, indicating **no extreme gender-based disparities** in overall academic performance.
* **Heatmap (Age & Year):** The slightly lower CGPA for the **25+ age group** suggests that maturity might not always translate to higher academic results, possibly due to other life commitments or returning to studies after a break. The consistency across admission years for younger groups shows stable academic standards.
* **Income & Scholarship:** The grouped bar plot confirms a powerful interaction effect: while higher income groups generally have higher CGPAs, the **Meritorious Scholarship** acts as a powerful equalizer and predictor of high performance, significantly boosting the average CGPA across **all income brackets**.
""")

st.caption("Dashboard section powered by Streamlit and Plotly.")

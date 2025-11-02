import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# Academic Performance Visualization Dashboard
# Objective 1: Socio-economic and Demographic Influence
# =========================================================

st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# Load Dataset
# =========================================================
@st.cache_data
def load_data():
    """Load academic performance dataset from GitHub."""
    try:
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20', '21-22', '23-24', '25+'], ordered=True)
        df['Income_Group'] = df['Income_Group'].astype(str)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Dataset could not be loaded or is missing required columns.")
    st.stop()

# =========================================================
# Objective Description
# =========================================================
st.header("Objective 1: Socio-economic and Demographic Influence")
st.markdown("🎓 **Goal:** Analyze the influence of socio-economic and demographic factors on student academic performance (Current CGPA).")

# =========================================================
# Summary Box (Top Section)
# =========================================================
st.subheader("📘 Summary Box: Socio-economic and Demographic Influence")

with st.container(border=True):
    st.markdown("""
    **Summary:**  
    This analysis explores the impact of **gender**, **age/admission year**, and **socio-economic status** on **Current CGPA**.  
    The visualizations show that while average CGPA is similar between genders, the **Meritorious Scholarship** status is a powerful positive differentiator across all income groups.  
    The heatmap reveals a potential academic challenge among older students (25+), as they tend to have slightly lower average CGPAs.  
    Overall, financial aid tied to merit appears to be a stronger predictor of academic performance than gender or income group alone.
    """)

st.divider()

# =========================================================
# Summary Metrics
# =========================================================
st.subheader("Key Summary Metrics for Academic Performance")

col1, col2, col3 = st.columns(3)
col1.metric("Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
col2.metric("Median CGPA", f"{df['Current_CGPA'].median():.2f}")
col3.metric("Std. Deviation", f"{df['Current_CGPA'].std():.2f}")

st.divider()

st.subheader("Average CGPA by Gender")

gender_cgpa = df.groupby('Gender', as_index=False)['Current_CGPA'].mean()
col_m, col_f = st.columns(2)

male_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Male', 'Current_CGPA'].squeeze() if 'Male' in gender_cgpa['Gender'].values else 0
female_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Female', 'Current_CGPA'].squeeze() if 'Female' in gender_cgpa['Gender'].values else 0

col_m.info(f"**Male Average CGPA:** {male_avg:.2f}")
col_f.info(f"**Female Average CGPA:** {female_avg:.2f}")

st.divider()

# =========================================================
# Visualization Functions
# =========================================================
def plot_cgpa_vs_gender(data):
    fig = px.box(
        data, x='Gender', y='Current_CGPA',
        color='Gender',
        title="CGPA Distribution by Gender",
        color_discrete_map={'Male': 'blue', 'Female': 'red'},
        height=450, range_y=[2.0, 4.0]
    )
    fig.update_layout(xaxis_title="Gender", yaxis_title="Current CGPA")
    return fig

def plot_cgpa_heatmap(data):
    grouped = data.groupby(['Admission_Year', 'Age_Group'])['Current_CGPA'].mean().unstack()
    fig = px.imshow(
        grouped,
        x=grouped.columns,
        y=grouped.index.astype(str),
        color_continuous_scale="YlGnBu",
        text_auto=".2f",
        title="Average CGPA by Admission Year and Age Group",
        height=500
    )
    fig.update_layout(xaxis_title="Age Group", yaxis_title="Admission Year")
    return fig

def plot_cgpa_by_income_scholarship(data):
    grouped = data.groupby(['Income_Group', 'Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        grouped,
        x='Income_Group',
        y='Current_CGPA',
        color='Meritorious_Scholarship',
        barmode='group',
        title="Average CGPA by Family Income and Scholarship Status",
        labels={'Current_CGPA': 'Average CGPA', 'Meritorious_Scholarship': 'Scholarship'},
        color_discrete_map={'Yes': 'green', 'No': 'red'},
        height=500
    )
    fig.update_layout(xaxis_title="Family Income Group", yaxis_title="Average CGPA")
    return fig

# =========================================================
# Visualizations + Interpretations
# =========================================================
st.subheader("Visualization 1: CGPA Distribution by Gender")
st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
* **Gender Parity:** The box plot and average metrics suggest that there is **no significant academic gap based on gender**.  
  Both male and female CGPA distributions are highly concentrated, indicating similar levels of academic success.
""")

st.divider()

st.subheader("Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")
st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
* **Age and Admission Year:** The **Heatmap** shows that the **Age Group (25+)** is associated with lower average CGPAs, 
  particularly for those admitted more recently (2020–2021).  
  This pattern might be due to non-traditional students balancing studies with external commitments (work, family), 
  which can affect time dedicated to coursework.
""")

st.divider()

st.subheader("Visualization 3: CGPA by Family Income Group and Scholarship Status")
st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
* **Scholarship as a Predictor:** The grouped bar plot confirms a powerful finding — students receiving a **Meritorious Scholarship** 
  maintain substantially higher CGPAs than their non-scholarship counterparts, *regardless of their family income group*.  
  This suggests that the selection criteria for the scholarship (which is merit-based) effectively identifies students with 
  the highest potential for academic excellence.
""")

st.success("✅ Analysis Completed Successfully")

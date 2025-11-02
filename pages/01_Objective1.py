import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 🎓 Academic Performance Visualization Dashboard
# Objective 1: Socio-economic and Demographic Influence
# =========================================================

st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 🧩 Load Dataset
# =========================================================
@st.cache_data
def load_data():
    """Load academic performance dataset from GitHub."""
    try:
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        df['Income_Group'] = df['Income_Group'].astype(str)
        return df
    except Exception as e:
        st.error(f"🚨 Failed to load dataset: {e}")
        return pd.DataFrame()

df = load_data()

# Validate Data
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("⚠️ Dataset could not be loaded or is missing required columns.")
    st.stop()

# =========================================================
# 🎯 Objective Description
# =========================================================
st.header("Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("""
🎓 **Goal:** Analyze the influence of socio-economic and demographic factors on student academic performance (**Current CGPA**).
""")

# =========================================================
# 📦 Summary Box (Moved to Top)
# =========================================================
st.subheader("📘 Summary Box: Socio-economic and Demographic Influence")

with st.container(border=True):
    st.markdown("""
    **Summary:**  
    This analysis explores the impact of **gender**, **age/admission year**, and **socio-economic status** on **Current CGPA**.  
    The visualizations show that while average CGPA is similar between genders (as reflected in the metrics), the **Meritorious Scholarship** status is a powerful positive differentiator across all income groups, consistently linking to higher average CGPA.  
    The heatmap reveals a potential academic challenge among older students (25+) across most admission years, as they tend to have slightly lower average CGPAs compared to the younger groups.  
    Overall, financial aid tied to merit appears to be a stronger predictor of academic performance than gender or income group alone.
    """)

st.divider()

# =========================================================
# 📊 Summary Metrics
# =========================================================
st.subheader("Key Summary Metrics for Academic Performance")

col1, col2, col3 = st.columns(3)
col1.metric("Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
col2.metric("Median CGPA", f"{df['Current_CGPA'].median():.2f}")
col3.metric("Std. Deviation", f"{df['Current_CGPA'].std():.2f}")

st.divider()

# --- Gender Metrics ---
st.subheader("Average CGPA by Gender")

gender_cgpa = df.groupby('Gender', as_index=False)['Current_CGPA'].mean()
col_m, col_f = st.columns(2)

male_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Male', 'Current_CGPA'].squeeze() if 'Male' in gender_cgpa['Gender'].values else 0
female_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Female', 'Current_CGPA'].squeeze() if 'Female' in gender_cgpa['Gender'].values else 0

col_m.info(f"**Male Average CGPA:** {male_avg:.2f}")
col_f.info(f"**Female Average CGPA:** {female_avg:.2f}")

st.divider()

# =========================================================
# 📈 Visualization Functions
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
        title="Average CGPA by Admission

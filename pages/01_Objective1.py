import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 🎓 Academic Performance Visualization Dashboard
# Objective 1: Socio-economic and Demographic Influence
# =========================================================

# --- Page Setup ---
st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Info ---
st.sidebar.title("📊 Dashboard Info")
st.sidebar.markdown("""
This dashboard analyzes how **socio-economic** and **demographic factors**  
influence **student academic performance (CGPA)**.

**Visualizations:**
1. CGPA Distribution by Gender  
2. Average CGPA by Admission Year & Age Group  
3. CGPA by Family Income & Scholarship Status
""")

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

# Load data
df = load_data()

# --- Validate Data ---
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("⚠️ Dataset could not be loaded or is missing required columns.")
    st.stop()

# =========================================================
# 📈 Overview & Key Metrics
# =========================================================
st.header("🎯 Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("""
This section explores how **gender**, **age**, **income**, and **scholarship status**
affect students’ **Current CGPA** performance.
""")

# --- Key CGPA Metrics ---
st.subheader("📊 Summary Metrics for Academic Performance")

col1, col2, col3 = st.columns(3)
col1.metric("Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
col2.metric("Median CGPA", f"{df['Current_CGPA'].median():.2f}")
col3.metric("Standard Deviation", f"{df['Current_CGPA'].std():.2f}")

st.divider()

# --- Gender Metrics ---
st.subheader("👩‍🎓 Average CGPA by Gender")

gender_cgpa = df.groupby('Gender', as_index=False)['Current_CGPA'].mean()
col_m, col_f = st.columns(2)

male_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Male', 'Current_CGPA'].squeeze() if 'Male' in gender_cgpa['Gender'].values else 0
female_avg = gender_cgpa.loc[gender_cgpa['Gender'] == 'Female', 'Current_CGPA'].squeeze() if 'Female' in gender_cgpa['Gender'].values else 0

col_m.info(f"**Male Average CGPA:** {male_avg:.2f}")
col_f.info(f"**Female Average CGPA:** {female_avg:.2f}")

st.divider()

# =========================================================
# 📊 Visualization Functions
# =========================================================
def plot_cgpa_vs_gender(data):
    fig = px.box(
        data, x='Gender', y='Current_CGPA',
        color='Gender',
        title="CGPA Distribution by Gender",
        color_discrete_map={'Male': 'royalblue', 'Female': 'lightcoral'},
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
        color_discrete_map={'Yes': 'seagreen', 'No': 'tomato'},
        height=500
    )
    fig.update_layout(xaxis_title="Family Income Group", yaxis_title="Average CGPA")
    return fig

# =========================================================
# 🧠 Visualizations
# =========================================================
st.subheader("📍 Visualization 1: CGPA Distribution by Gender")
st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)

st.subheader("📍 Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")
st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)

st.subheader("📍 Visualization 3: CGPA by Family Income and Scholarship Status")
st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)

# =========================================================
# 🧩 Findings and Interpretation
# =========================================================
st.header("🔍 Analysis and Findings", divider="blue")

with st.container(border=True):
    st.markdown("""
    **Summary:**  
    This analysis explores the impact of **gender**, **age**, and **socio-economic background** 
    on academic performance. Results show that:
    
    - **Gender parity** exists in academic outcomes.  
    - **Older students (25+)** often have slightly lower CGPAs, possibly due to additional life commitments.  
    - **Meritorious scholarships** consistently align with higher CGPAs across all income levels, 
      indicating their strong link to student performance and potential.
    """)

st.markdown("""
**Interpretation Highlights:**
- 🎯 *Gender Equality:* CGPA differences between genders are minimal.  
- 🧑‍🏫 *Age & Admission Year:* Non-traditional or older students show modestly lower averages.  
- 💰 *Scholarship Effect:* Scholarship recipients outperform peers in every income group.
""")

# =========================================================
# ✅ End of Page
# =========================================================
st.success("✅ Analysis Completed Successfully")


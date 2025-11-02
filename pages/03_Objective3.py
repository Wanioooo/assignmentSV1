import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide")

# --- Load Data Function ---
@st.cache_data
def load_data():
    try:
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)

        # Ensure consistent category ordering
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20', '21-22', '23-24', '25+'], ordered=True)
        
        # Sort categories for better visual order
        study_order = sorted(df['Daily_Study_Hours'].unique())
        media_order = sorted(df['Daily_Social_Media_Hours'].unique())

        df['Daily_Study_Hours'] = pd.Categorical(df['Daily_Study_Hours'], categories=study_order, ordered=True)
        df['Daily_Social_Media_Hours'] = pd.Categorical(df['Daily_Social_Media_Hours'], categories=media_order, ordered=True)

        return df
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred during data loading: {e}")
        return pd.DataFrame({
            'Current_CGPA': [], 'Daily_Study_Hours': [], 'Daily_Social_Media_Hours': [],
            'Attendance_Pct': [], 'Learning_Mode': [], 'Has_PC': []
        })

# --- Load Data ---
df = load_data()

st.title("Objective 2: Study Habits and Resource Utilization")
st.markdown("🔍 Investigate the relationship between study habits and resource utilization with student academic performance.")

# --- Summary Metrics Section ---
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    st.stop()

st.header("Key Summary Metrics", divider="blue")

col1, col2, col3 = st.columns(3)
col1.metric("Overall Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
col2.metric("Average Attendance %", f"{df['Attendance_Pct'].mean():.1f}%")

correlation = df['Attendance_Pct'].corr(df['Current_CGPA'])
col3.metric(
    "Attendance vs. CGPA Correlation",
    f"{correlation:.2f}",
    help="Pearson correlation coefficient between Class Attendance Percentage and Current CGPA."
)

st.subheader("CGPA by Study vs. Social Media Balance")

# --- Study/Social Media Insights ---
study_cgpa = df.groupby('Daily_Study_Hours')['Current_CGPA'].mean().sort_values(ascending=False)
social_cgpa = df.groupby('Daily_Social_Media_Hours')['Current_CGPA'].mean().sort_values(ascending=True)

col_study, col_social, col_pc = st.columns(3)

col_study.metric(
    label=f"Highest Avg. CGPA ({study_cgpa.index[0]} Study Hours)",
    value=f"{study_cgpa.iloc[0]:.2f}"
)

col_social.metric(
    label=f"Lowest Avg. CGPA ({social_cgpa.index[0]} Social Media Hours)",
    value=f"{social_cgpa.iloc[0]:.2f}"
)

pc_data = df.groupby('Has_PC')['Current_CGPA'].mean()
if 'Yes' in pc_data.index and 'No' in pc_data.index:
    pc_diff = pc_data['Yes'] - pc_data['No']
    col_pc.metric(
        label="CGPA Difference (PC Ownership)",
        value=f"{pc_diff:.2f}",
        delta="Higher" if pc_diff > 0 else "Lower",
        help="Average CGPA difference between students with and without personal computers."
    )

st.divider()

# --- Summary Box (Before Visualizations) ---
st.header("📦 Summary Box: Study Habits and Resource Utilization", divider="gray")
with st.container(border=True):
    st.markdown("""
    **Summary:**
    This objective analyzes how *study habits* (study time, social media time, attendance) and *resources* (PC ownership) impact *Current CGPA*.  
    There is a clear **positive relationship** between *Daily Study Hours* and *Average CGPA*, peaking in the 3–4 hour range.  
    Conversely, increased *Daily Social Media Hours* correlate with lower median CGPA and higher variability.  
    The scatter plot confirms a **strong positive correlation** (~0.70) between *Class Attendance Percentage* and *CGPA*, showing its importance for academic success.  
    Furthermore, owning a *Personal Computer (PC)* is associated with consistently higher average CGPA across all learning modes, highlighting the academic advantage of access to digital resources.
    """)

# --- Visualization 1 ---
st.subheader("Visualization 1: CGPA Distribution by Daily Social Media Hours")
fig1 = px.box(
    df,
    x='Daily_Social_Media_Hours',
    y='Current_CGPA',
    color='Daily_Social_Media_Hours',
    title='Visualization 1: CGPA Distribution by Daily Social Media Hours',
    height=550,
    range_y=[2.0, 4.0]
)
fig1.update_layout(
    xaxis_title='Daily Social Media Hours (Hours)',
    yaxis_title='Current CGPA',
    showlegend=False
)
st.plotly_chart(fig1, use_container_width=True)
st.markdown("""
**Interpretation:**  
Higher daily social media usage corresponds to a lower median CGPA and increased performance variability.  
This pattern suggests that excessive social media engagement is linked with *reduced academic focus and consistency*.
""")

# --- Visualization 2 ---
st.subheader("Visualization 2: Scatter Plot of Current CGPA vs. Class Attendance Percentage")
fig2 = px.scatter(
    df,
    x='Attendance_Pct',
    y='Current_CGPA',
    trendline='ols',
    title='Visualization 2: Scatter Plot of Current CGPA vs. Class Attendance Percentage',
    height=500,
    range_x=[0, 100],
    range_y=[2.0, 4.0]
)
fig2.update_layout(
    xaxis_title='Class Attendance Percentage',
    yaxis_title='Current CGPA'
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown("""
**Interpretation:**  
The scatter plot exhibits a strong **positive correlation** between *Class Attendance* and *CGPA*.  
Students with consistent attendance generally maintain higher academic performance, confirming that *class participation and presence* are essential to success.
""")

# --- Visualization 3 ---
st.subheader("Visualization 4: Average CGPA: PC Ownership vs. Learning Mode")
pc_mode_data = df.groupby(['Learning_Mode', 'Has_PC'])['Current_CGPA'].mean().reset_index()
fig4 = px.bar(
    pc_mode_data,
    x='Learning_Mode',
    y='Current_CGPA',
    color='Has_PC',
    barmode='group',
    title='Visualization 4: Average CGPA: PC Ownership vs. Learning Mode',
    labels={'Current_CGPA': 'Average Current CGPA', 'Has_PC': 'Has Personal Computer?'},
    height=500,
    color_discrete_map={'Yes': '#E41A1C', 'No': '#377EB8'}
)
fig4.update_layout(
    xaxis_title='Preferred Learning Mode',
    yaxis_title='Average Current CGPA'
)
st.plotly_chart(fig4, use_container_width=True)
st.markdown("""
**Interpretation:**  
Students who own a **Personal Computer (PC)** consistently show higher CGPA across all learning modes (online, physical, blended).  
This finding emphasizes how *access to technology* significantly supports academic performance and efficiency.
""")

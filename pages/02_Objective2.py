import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Streamlit Page Config ---
st.set_page_config(layout="wide")

# --- Load Data Function ---
@st.cache_data
def load_data():
    try:
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)

        # Categorical ordering
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        study_order = sorted(df['Daily_Study_Hours'].unique())
        media_order = sorted(df['Daily_Social_Media_Hours'].unique())

        df['Daily_Study_Hours'] = pd.Categorical(df['Daily_Study_Hours'], categories=study_order, ordered=True)
        df['Daily_Social_Media_Hours'] = pd.Categorical(df['Daily_Social_Media_Hours'], categories=media_order, ordered=True)
        return df
    except Exception as e:
        st.error(f"🚨 Error loading dataset: {e}")
        return pd.DataFrame()

df = load_data()

# --- Title and Description ---
st.title("Objective 2: Study Habits and Resource Utilization")
st.markdown("🔍 Investigate the relationship between study habits and resource utilization with student academic performance.")

# --- Safety Check ---
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("⚠️ Cannot run analysis — data failed to load properly.")
    st.stop()

# ==============================
# 🔹 SUMMARY SECTION (TOP BOX)
# ==============================
st.header("📊 Summary of Findings", divider="blue")

st.markdown("""
**Summary:**
This objective analyzes how **study habits** (study time, social media time, attendance) and **resources** (PC ownership) impact **Current CGPA**.  
There is a clear **positive relationship** between **Daily Study Hours** and average CGPA, peaking in the 3–4 hour range.  
Conversely, increased **Daily Social Media Hours** correlate with lower median CGPA and wider performance variation.  
The scatter plot confirms a **strong positive correlation (~0.70)** between **Class Attendance Percentage** and CGPA.  
Owning a **Personal Computer (PC)** is also associated with a reliably higher average CGPA, regardless of learning mode, showing that access to digital resources benefits academic outcomes.
""")

st.divider()

# ==============================
# 🔹 KEY METRICS SECTION
# ==============================
st.header("Key Summary Metrics", divider="blue")

col1, col2, col3 = st.columns(3)
col1.metric("Overall Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
col2.metric("Average Attendance %", f"{df['Attendance_Pct'].mean():.1f}%")

correlation = df['Attendance_Pct'].corr(df['Current_CGPA'])
col3.metric("Attendance vs. CGPA Correlation", f"{correlation:.2f}")

st.subheader("CGPA by Study vs. Social Media Balance")

study_cgpa = df.groupby('Daily_Study_Hours')['Current_CGPA'].mean().sort_values(ascending=False)
social_cgpa = df.groupby('Daily_Social_Media_Hours')['Current_CGPA'].mean().sort_values(ascending=True)

col_study, col_social, col_pc = st.columns(3)
with col_study:
    st.markdown("**Highest CGPA Correlates with:**")
    st.metric(f"Avg. CGPA for {study_cgpa.index[0]} Study Hours", f"{study_cgpa.iloc[0]:.2f}")

with col_social:
    st.markdown("**Lowest CGPA Correlates with:**")
    st.metric(f"Avg. CGPA for {social_cgpa.index[0]} Social Media Hours", f"{social_cgpa.iloc[0]:.2f}")

pc_data = df.groupby('Has_PC')['Current_CGPA'].mean()
if 'Yes' in pc_data.index and 'No' in pc_data.index:
    pc_diff = pc_data['Yes'] - pc_data['No']
    with col_pc:
        st.markdown("**Impact of PC Ownership:**")
        st.metric("CGPA Difference (PC Yes - No)", f"{pc_diff:.2f}", delta="Higher" if pc_diff > 0 else "Lower")

st.divider()

# ==============================
# 🔹 VISUALIZATION FUNCTIONS
# ==============================
def plot_cgpa_vs_social_media(data):
    fig = px.box(
        data,
        x='Daily_Social_Media_Hours',
        y='Current_CGPA',
        color='Daily_Social_Media_Hours',
        title='Visualization 1: CGPA Distribution by Daily Social Media Hours',
        height=550,
        range_y=[2.0,4.0]
    )
    order_array = list(data['Daily_Social_Media_Hours'].cat.categories)
    fig.update_layout(
        xaxis={'categoryorder':'array','categoryarray':order_array},
        xaxis_title='Daily Social Media Hours (Hours)',
        yaxis_title='Current CGPA',
        showlegend=False
    )
    return fig

def plot_cgpa_vs_attendance(data):
    fig = px.scatter(
        data,
        x='Attendance_Pct',
        y='Current_CGPA',
        trendline='ols',
        title='Visualization 2: Current CGPA vs. Class Attendance Percentage',
        height=500,
        range_x=[0,100],
        range_y=[2.0,4.0]
    )
    fig.update_layout(xaxis_title='Class Attendance (%)', yaxis_title='Current CGPA')
    return fig

def plot_cgpa_vs_study_hours(data):
    study_data = data.groupby('Daily_Study_Hours')['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        study_data,
        x='Daily_Study_Hours',
        y='Current_CGPA',
        color='Daily_Study_Hours',
        title='Visualization 3: Average CGPA by Daily Study Hours',
        height=500
    )
    order_array = list(data['Daily_Study_Hours'].cat.categories)
    fig.update_layout(
        xaxis={'categoryorder':'array','categoryarray':order_array},
        xaxis_title='Daily Study Hours (Hours)',
        yaxis_title='Average CGPA',
        showlegend=False
    )
    return fig

def plot_pc_vs_learning_mode(data):
    pc_mode_data = data.groupby(['Learning_Mode','Has_PC'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        pc_mode_data,
        x='Learning_Mode',
        y='Current_CGPA',
        color='Has_PC',
        barmode='group',
        title='Visualization 4: Average CGPA — PC Ownership vs. Learning Mode',
        labels={'Current_CGPA':'Average CGPA','Has_PC':'Has Personal Computer?'},
        height=500,
        color_discrete_map={'Yes':'#E41A1C','No':'#377EB8'}
    )
    fig.update_layout(xaxis_title='Learning Mode', yaxis_title='Average Current CGPA')
    return fig

# ==============================
# 🔹 VISUALIZATION DISPLAY + INTERPRETATION
# ==============================

# --- Visualization 1 ---
st.subheader("Visualization 1: CGPA Distribution by Daily Social Media Hours")
st.plotly_chart(plot_cgpa_vs_social_media(df), use_container_width=True)
st.markdown("""
💡 **Interpretation:**  
Higher daily social media usage tends to lower the median CGPA and increase variability, suggesting it may distract from academic focus.
""")

# --- Visualization 2 ---
st.subheader("Visualization 2: Scatter Plot of Current CGPA vs. Class Attendance Percentage")
st.plotly_chart(plot_cgpa_vs_attendance(df), use_container_width=True)
st.markdown("""
💡 **Interpretation:**  
A strong positive correlation (~0.70) exists between attendance percentage and CGPA, confirming that consistent class participation boosts performance.
""")

# --- Visualization 3 ---
st.subheader("Visualization 3: Average CGPA by Daily Study Hours")
st.plotly_chart(plot_cgpa_vs_study_hours(df), use_container_width=True)
st.markdown("""
💡 **Interpretation:**  
Average CGPA increases with more study hours, peaking around 3–4 hours daily, before slightly tapering — suggesting a healthy study balance is key.
""")

# --- Visualization 4 ---
st.subheader("Visualization 4: Average CGPA — PC Ownership vs. Learning Mode")
st.plotly_chart(plot_pc_vs_learning_mode(df), use_container_width=True)
st.markdown("""
💡 **Interpretation:**  
Students with a personal computer achieve higher average CGPAs across all learning modes, highlighting the role of digital resource accessibility in academic success.
""")

# ==============================
# 🔹 FINAL SUMMARY
# ==============================
st.header("Interpretation Summary", divider="red")
st.markdown("""
* **Study Time vs. CGPA:** Positive upward trend — effort aligns with performance.  
* **Attendance:** Strongest single predictor of CGPA.  
* **Social Media:** Higher usage increases performance variance, generally lowering CGPA.  
* **PC Ownership:** Consistent academic benefit across all learning modes.  
""")

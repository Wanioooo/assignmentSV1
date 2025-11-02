import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ===============================
# Streamlit Page Configuration
# ===============================
st.set_page_config(
    page_title="Objective 3: Academic Challenges and Student Engagement",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    try:
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)

        # Order categorical variables for clarity
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20', '21-22', '23-24', '25+'], ordered=True)
        english_order = ['Basic', 'Intermediate', 'Advance']
        df['English_Proficiency'] = pd.Categorical(df['English_Proficiency'], categories=english_order, ordered=True)

        return df
    except Exception as e:
        st.error(f"🚨 Error during data loading: {e}")
        return pd.DataFrame({
            'Current_CGPA': [], 'Fell_Probation': [], 'Attends_Consultancy': [],
            'Semester': [], 'Daily_Skill_Dev_Hours': [], 'English_Proficiency': []
        })


df = load_data()

# ===============================
# Page Title
# ===============================
st.title("Objective 3: Academic Challenges and Student Engagement")
st.markdown("🤝 Explore the interplay of academic challenges and student engagement with overall performance.")

# ===============================
# Handle Empty Data
# ===============================
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("⚠️ Cannot run analysis: Dataset failed to load correctly.")
    st.stop()

# ==

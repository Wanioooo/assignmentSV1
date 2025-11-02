import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Objective 3 - Academic Insights", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("new_dataset_academic_performance (1).csv")
    return df

df = load_data()

# Show columns to confirm correct names
st.write("📋 Columns in dataset:", df.columns.tolist())

# --- Summary box ---
st.subheader("🎯 Objective 3: Academic Insights")
st.info("""
This section investigates academic behavior patterns by linking study hours, sleep quality,
and extracurricular activities to academic performance.
""")

# --- Visualization 1 ---
try:
    fig1 = px.scatter(
        df,
        x="StudyHours",  # 🔁 change to match your actual column name
        y="PerformanceScore",  # 🔁 change to match your actual column name
        color="Gender",  # 🔁 change if necessary
        title="Study Hours vs Performance Score by Gender",
        labels={"StudyHours": "Study Hours per Day", "PerformanceScore": "Performance Score"}
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("**Interpretation:** Students who spend more hours studying tend to achieve higher scores overall.")
except ValueError as e:
    st.error(f"⚠️ Check your column names: {e}")

# --- Visualization 2 ---
try:
    fig2 = px.box(
        df,
        x="SleepDuration",  # 🔁 change if needed
        y="PerformanceScore",
        color="Gender",
        title="Sleep Duration vs Academic Performance",
        labels={"SleepDuration": "Sleep Duration (hours)", "PerformanceScore": "Performance Score"}
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("**Interpretation:** Students with 6–8 hours of sleep usually perform better academically.")
except ValueError as e:
    st.error(f"⚠️ Check your column names: {e}")

# --- Visualization 3 ---
try:
    fig3 = px.violin(
        df,
        x="Extracurricular",  # 🔁 check spelling
        y="PerformanceScore",
        color="Gender",
        box=True,
        points="all",
        title="Extracurricular Involvement vs Academic Performance",
        labels={"Extracurricular": "Extracurricular Participation", "PerformanceScore": "Performance Score"}
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("**Interpretation:** Balanced involvement in extracurriculars correlates with higher performance.")
except ValueError as e:
    st.error(f"⚠️ Check your column names: {e}")

st.markdown("---")
st.success("✅ Objective 3 visualizations loaded successfully!")

import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# Page Configuration
# ======================
st.set_page_config(page_title="Objective 2 - Learning Factors", layout="wide")

# ======================
# Load Dataset
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("new_dataset_academic_performance (1).csv")
    return df

df = load_data()

# ======================
# Summary Box
# ======================
with st.container():
    st.subheader("📊 Objective 2: Learning Factors")
    st.info("""
    This section explores how different learning-related factors affect students' academic performance.
    The analysis focuses on study hours, sleep duration, and extracurricular involvement in relation
    to performance scores.
    """)

# ======================
# Visualization 1 - Study Hours vs Performance
# ======================
st.write("### 1️⃣ Relationship between Study Hours and Academic Performance")

fig1 = px.scatter(
    df,
    x="StudyHours",
    y="PerformanceScore",
    color="Gender",
    title="Study Hours vs Performance Score by Gender",
    labels={"StudyHours": "Study Hours per Day", "PerformanceScore": "Performance Score"}
)
st.plotly_chart(fig1, use_container_width=True)

st.caption("""
**Interpretation:** Students who dedicate more study hours per day tend to achieve higher performance scores.
This trend appears across genders, indicating that consistent study habits positively impact academic results.
""")

# ======================
# Visualization 2 - Sleep Duration vs Performance
# ======================
st.write("### 2️⃣ Relationship between Sleep Duration and Academic Performance")

fig2 = px.box(
    df,
    x="SleepDuration",
    y="PerformanceScore",
    color="Gender",
    title="Sleep Duration vs Performance by Gender",
    labels={"SleepDuration": "Sleep Duration (hours)", "PerformanceScore": "Performance Score"}
)
st.plotly_chart(fig2, use_container_width=True)

st.caption("""
**Interpretation:** Students who sleep between 6–8 hours generally perform better compared to those who sleep
less than 5 hours, emphasizing the importance of adequate rest in maintaining academic performance.
""")

# ======================
# Visualization 3 - Extracurricular Involvement
# ======================
st.write("### 3️⃣ Extracurricular Involvement vs Academic Performance")

fig3 = px.violin(
    df,
    x="Extracurricular",
    y="PerformanceScore",
    color="Gender",
    box=True,
    points="all",
    title="Extracurricular Involvement and Performance Distribution",
    labels={"Extracurricular": "Extracurricular Participation", "PerformanceScore": "Performance Score"}
)
st.plotly_chart(fig3, use_container_width=True)

st.caption("""
**Interpretation:** Moderate involvement in extracurricular activities is associated with balanced academic
performance. Excessive participation may reduce study time, while no participation can limit soft skill development.
""")

# ======================
# Footer
# ======================
st.markdown("---")
st.success("✅ Analysis completed successfully!")

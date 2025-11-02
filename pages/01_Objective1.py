import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ... (Load Data Function) ...
# ... (DataFrame loading) ...

st.header("Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("🎓 Analyze the influence of socio-economic and demographic factors on student academic performance (Current CGPA). ")

# --- START: Summary Metrics Section ---
st.subheader("Key Summary Metrics for Academic Performance")

# 1. Overall CGPA Metrics
avg_cgpa = df['Current_CGPA'].mean()
median_cgpa = df['Current_CGPA'].median()
std_cgpa = df['Current_CGPA'].std()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Current CGPA (Overall)", value=f"{avg_cgpa:.2f}")

with col2:
    st.metric(label="Median Current CGPA (Overall)", value=f"{median_cgpa:.2f}")

with col3:
    st.metric(label="Std. Dev. of Current CGPA", value=f"{std_cgpa:.2f}")

st.divider()

# 2. Gender-Specific Metrics
st.subheader("Average CGPA by Gender")
gender_cgpa = df.groupby('Gender')['Current_CGPA'].mean().reset_index()

col_m, col_f = st.columns(2)

male_avg = gender_cgpa[gender_cgpa['Gender'] == 'Male']['Current_CGPA'].iloc[0]
female_avg = gender_cgpa[gender_cgpa['Gender'] == 'Female']['Current_CGPA'].iloc[0]

with col_m:
    st.info(f"**Male Average CGPA:** {male_avg:.2f}")

with col_f:
    st.info(f"**Female Average CGPA:** {female_avg:.2f}")
    
st.divider()
# --- END: Summary Metrics Section ---

# --- Visualization Functions from main.py ---
# ... (Define plot_cgpa_vs_gender, plot_cgpa_heatmap, plot_cgpa_by_income_scholarship) ...

# --- Display the 3 visualizations ---
st.subheader("Visualization 1: Box Plot of CGPA Distribution by Gender")
st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True) # use_container_width is often better than width='stretch'
st.subheader("Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")
st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)
st.subheader("Visualization 3: Group Bar Plot Average CGPA by Family Income Group and Meritorious Scholarship Status.")
st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)

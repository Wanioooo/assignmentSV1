import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('new_dataset_academic_performance (1).csv')
    return df

df = load_data()

# --- Page Title ---
st.title("Objective 1: Core Demographics")

# --- 1. CGPA vs Gender ---
st.subheader("1️⃣ CGPA Distribution by Gender")
fig1 = px.box(df, x='Gender', y='Current_CGPA', color='Gender',
              color_discrete_map={'Male':'blue', 'Female':'red'})
st.plotly_chart(fig1, width='stretch')

# --- 2. CGPA vs Age Group ---
st.subheader("2️⃣ CGPA Distribution by Age Group")
fig2 = px.box(df, x='Age_Group', y='Current_CGPA', color='Age_Group')
st.plotly_chart(fig2, width='stretch')

# --- 3. Average CGPA by Admission Year ---
st.subheader("3️⃣ Average CGPA by Admission Year")
avg_cgpa = df.groupby('Admission_Year')['Current_CGPA'].mean().reset_index()
fig3 = px.bar(avg_cgpa, x='Admission_Year', y='Current_CGPA', 
              labels={'Current_CGPA':'Average CGPA', 'Admission_Year':'Admission Year'})
st.plotly_chart(fig3, width='stretch')

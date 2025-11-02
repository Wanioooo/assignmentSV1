import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

URL="https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"

# --- Configuration (Set page layout early) ---
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    # Since the specific CSV is unavailable, we create a mock DataFrame 
    # that matches the columns and logic used in the visualization functions.
    
    # Define categories
    age_groups = ['18-20','21-22','23-24','25+']
    genders = ['Male', 'Female']
    years = [2021, 2022, 2023]
    scholarship = ['Yes', 'No']
    income = ['Low', 'Medium', 'High']

    # Generate mock data
    np.random.seed(42)
    data = {
        'Current_CGPA': np.random.uniform(2.5, 3.8, 100).round(2),
        'Gender': np.random.choice(genders, 100),
        'Age_Group': np.random.choice(age_groups, 100),
        'Admission_Year': np.random.choice(years, 100),
        'Meritorious_Scholarship': np.random.choice(scholarship, 100),
        'Income_Group': np.random.choice(income, 100),
    }
    df = pd.DataFrame(data)
    
    # Make sure categories are ordered correctly
    df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=age_groups, ordered=True)
    df['Income_Group'] = pd.Categorical(df['Income_Group'], categories=income, ordered=True)
    
    st.info("⚠️ Using Mock Data: The original CSV file was unavailable, so a mock dataset was created for demonstration.")
    return df

df = load_data()

st.header("Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("🎓 Analyze the influence of socio-economic and demographic factors on student academic performance (Current CGPA). ")

# --- Visualization Functions (Defined once) ---

def plot_cgpa_vs_gender(data):
    fig = px.box(
        data,
        x='Gender',
        y='Current_CGPA',
        title='CGPA Distribution by Gender',
        color='Gender',
        color_discrete_map={'Male':'#1f77b4','Female':'#ff7f0e'}, # Use professional colors
        height=450,
        range_y=[2.0,4.0]
    )
    fig.update_layout(xaxis_title='Gender', yaxis_title='Current CGPA')
    return fig

def plot_cgpa_heatmap(data):
    heatmap_data = data.groupby(['Admission_Year','Age_Group'])['Current_CGPA'].mean().unstack()
    age_order = ['18-20','21-22','23-24','25+']
    heatmap_data = heatmap_data.reindex(columns=age_order)
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index.astype(str),
        color_continuous_scale="Viridis", # Using Viridis for better contrast
        aspect="auto",
        text_auto=".2f",
        title='Average CGPA by Admission Year and Age Group'
    )
    fig.update_layout(xaxis_title='Age Group (Years)', yaxis_title='University Admission Year', height=500)
    fig.update_coloraxes(colorbar_title='Average Current CGPA')
    return fig
    
def plot_cgpa_by_income_scholarship(data):
    grouped_data = data.groupby(['Income_Group','Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        grouped_data,
        x='Income_Group',
        y='Current_CGPA',
        color='Meritorious_Scholarship',
        barmode='group',
        title='Average CGPA by Family Income Group and Meritorious Scholarship Status',
        labels={'Current_CGPA':'Average Current CGPA','Meritorious_Scholarship':'Meritorious Scholarship?'},
        height=500,
        color_discrete_map={'Yes':'#2ca02c','No':'#d62728'} # Use professional colors
    )
    fig.update_layout(xaxis_title='Family Income Group', yaxis_title='Average Current CGPA')
    return fig

# --- Display the 3 visualizations (The correct order) ---

# Visualization 1
st.subheader("Visualization 1: Box Plot of CGPA Distribution by Gender")
st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)

st.divider()

# Visualization 2
st.subheader("Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")
st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)

st.divider()

# Visualization 3
st.subheader("Visualization 3: Group Bar Plot Average CGPA by Family Income Group and Meritorious Scholarship Status.")
st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)

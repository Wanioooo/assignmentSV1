import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration for better layout (optional, but good practice)
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        # *CRITICAL FIX: Check this file path is correct in your Streamlit environment*
        df = pd.read_csv('new_dataset_academic_performance (1).csv')
        
        # Optional: make sure categories are ordered
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        return df
    except FileNotFoundError:
        st.error("🚨 Error: Data file 'new_dataset_academic_performance (1).csv' not found. Please ensure it is in the correct path.")
        # Return an empty DataFrame to prevent NameError in the rest of the script
        return pd.DataFrame({'Current_CGPA': [], 'Gender': [], 'Admission_Year': [], 'Age_Group': [], 'Income_Group': [], 'Meritorious_Scholarship': []})
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred during data loading: {e}")
        return pd.DataFrame({'Current_CGPA': [], 'Gender': [], 'Admission_Year': [], 'Age_Group': [], 'Income_Group': [], 'Meritorious_Scholarship': []})

df = load_data()

# Check if the DataFrame is empty before proceeding with calculations
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    st.stop() # Stop execution if data is invalid

# --- App Content Starts Here ---

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

# Ensure 'Male' and 'Female' exist before trying to access them
male_avg = gender_cgpa[gender_cgpa['Gender'] == 'Male']['Current_CGPA'].iloc[0] if 'Male' in gender_cgpa['Gender'].values else 0.00
female_avg = gender_cgpa[gender_cgpa['Gender'] == 'Female']['Current_CGPA'].iloc[0] if 'Female' in gender_cgpa['Gender'].values else 0.00

with col_m:
    st.info(f"*Male Average CGPA:* {male_avg:.2f}")

with col_f:
    st.info(f"*Female Average CGPA:* {female_avg:.2f}")
    
st.divider()
# --- END: Summary Metrics Section ---


# --- Visualization Functions (kept exactly as you provided) ---

def plot_cgpa_vs_gender(data):
    fig = px.box(
        data,
        x='Gender',
        y='Current_CGPA',
        title='CGPA Distribution by Gender',
        color='Gender',
        color_discrete_map={'Male':'blue','Female':'red'},
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

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

import streamlit as st

# Note: st.set_page_config is only needed in the main file (main.py)

# You can set a custom title for the sidebar here (optional)
# Streamlit will automatically use the filename (Objective 1)
st.title("🎯 Objective 1: Data Exploration and Cleaning")
st.header("Initial Data Assessment")

st.markdown("""
This page focuses on loading the data, checking for missing values, 
understanding data types, and performing necessary cleaning steps.

---

### Step 1: Data Loading
*Code block to load `new_dataset_academic_performance (1).csv`.*

### Step 2: Distribution Analysis
*Visualizations like histograms and box plots for key numeric columns (e.g., scores).*

### Step 3: Cleaning and Transformation
*Logic for handling outliers, encoding categorical variables, etc.*
""")

# Example of a chart placeholder
st.subheader("Distribution of Math Scores")
st.bar_chart({'Math Score': [60, 70, 80, 90, 100], 'Count': [5, 15, 25, 10, 5]})


# --- 1. Configuration and Data Loading ---

st.title("📊 Academic Performance Analysis")

# Define the URL of the CSV file
URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"

@st.cache_data
def load_data(data_url):
    """Loads, cleans, and prepares the DataFrame."""
    try:
        df = pd.read_csv(data_url)
        
        # --- Essential Data Preprocessing for plotting ---
        # Convert grouping columns to string/categorical to ensure correct plotting behavior
        if 'Admission_Year' in df.columns:
            df['Admission_Year'] = df['Admission_Year'].astype(str)
        if 'Age_Group' in df.columns:
            df['Age_Group'] = df['Age_Group'].astype(str)
            
        # Define and apply the correct order for the Age_Group (Critical for Heatmap)
        age_order = ['18-20', '21-22', '23-24', '25+']
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=age_order, ordered=True)
            
        return df
    except Exception as e:
        st.error(f"Error loading or preparing data. Please check the URL and column names.")
        st.exception(e) # Show the detailed error for debugging
        return pd.DataFrame()

df = load_data(URL)

if df.empty:
    st.stop() # Stop the app if data loading failed

# Optional: Display raw data in an expander for confirmation
with st.expander("🔍 View Data and Column Check"):
    st.dataframe(df)
    st.write(f"DataFrame Shape: {df.shape}")
    st.write("Column Names and Data Types:")
    st.dataframe(df.dtypes)

# --- 2. Visualizations using Plotly Express ---
st.header("Visualizations")

col1, col2 = st.columns(2)

# --- Box Plot: Current CGPA vs. Gender ---
with col1:
    st.subheader("1. CGPA Distribution by Gender (Box Plot)")
    if all(c in df.columns for c in ['Gender', 'Current_CGPA']):
        fig1 = px.box(
            df,
            x='Gender',
            y='Current_CGPA',
            title='CGPA Distribution by Gender',
            color='Gender',
            labels={'Current_CGPA': 'Current CGPA'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_yaxes(range=[2.0, 4.0], autorange=False)
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Skipping Box Plot: 'Gender' or 'Current_CGPA' column not found.")

# --- Violin Plot: CGPA across University Admission Years ---
with col2:
    st.subheader("2. CGPA Distribution across Admission Years (Violin Plot)")
    if all(c in df.columns for c in ['Admission_Year', 'Current_CGPA']):
        fig2 = px.violin(
            df, 
            x='Admission_Year', 
            y='Current_CGPA', 
            color='Admission_Year',
            box=True, 
            points='all', # Showing all points is often more informative
            title='Distribution of Current CGPA across University Admission Years',
            labels={'Current_CGPA': 'Current CGPA'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_yaxes(range=[2.0, 4.0], autorange=False)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Skipping Violin Plot: 'Admission_Year' or 'Current_CGPA' column not found.")

st.markdown("---")

# --- Heatmap: Average CGPA by Admission Year and Age Group ---
st.subheader("3. Average CGPA by Admission Year and Age Group (Heatmap)")
if all(c in df.columns for c in ['Admission_Year', 'Age_Group', 'Current_CGPA']):
    # Prepare data for heatmap
    heatmap_data_grouped = df.groupby(['Admission_Year', 'Age_Group'])['Current_CGPA'].mean().unstack()

    # Reindex columns to ensure correct order
    age_order = ['18-20', '21-22', '23-24', '25+']
    heatmap_data_grouped = heatmap_data_grouped.reindex(columns=age_order)
    
    # Plotly Express Heatmap
    fig3 = px.imshow(
        heatmap_data_grouped, # Pass the DataFrame directly to px.imshow
        x=heatmap_data_grouped.columns.tolist(),
        y=heatmap_data_grouped.index.tolist(),
        color_continuous_scale="YlGnBu",
        text_auto=".2f",
        aspect="auto",
        title='Average CGPA by Admission Year and Age Group'
    )

    fig3.update_layout(
        xaxis_title='Age Group (Years)',
        yaxis_title='University Admission Year',
        xaxis={'side': 'bottom'}
    )
    fig3.update_coloraxes(colorbar_title='Average Current CGPA')

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Skipping Heatmap: Required columns ('Admission_Year', 'Age_Group', 'Current_CGPA') not found.")

st.markdown("---")

# --- Grouped Bar Plot: Average CGPA by Income Group and Scholarship ---
st.subheader("4. Average CGPA by Income Group and Meritorious Scholarship")
if all(c in df.columns for c in ['Income_Group', 'Meritorious_Scholarship', 'Current_CGPA']):
    # Calculate the average CGPA
    grouped_data_bar = df.groupby(['Income_Group', 'Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()

    # Plotly Express Grouped Bar Chart
    fig4 = px.bar(
        grouped_data_bar, 
        x='Income_Group', 
        y='Current_CGPA', 
        color='Meritorious_Scholarship', 
        barmode='group', # Creates the grouped bars
        title='Average CGPA by Family Income Group and Meritorious Scholarship Status',
        labels={'Current_CGPA': 'Average Current CGPA', 'Income_Group': 'Family Income Group', 'Meritorious_Scholarship': 'Meritorious Scholarship'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("Skipping Bar Plot: Required columns ('Income_Group', 'Meritorious_Scholarship', 'Current_CGPA') not found.")

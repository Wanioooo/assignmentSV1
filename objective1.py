import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. Data Loading and Setup ---
st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Academic Performance Analysis")
st.markdown("Exploring the distribution of **Current CGPA** across various demographic and academic factors using Plotly in Streamlit.")

# Define the URL of the CSV file
url = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"

@st.cache_data # Cache the data loading to improve performance
def load_data(data_url):
    try:
        df = pd.read_csv(data_url)
        # Ensure Age_Group is a string for plotting/grouping
        df['Age_Group'] = df['Age_Group'].astype(str)
        # Assuming 'Admission_Year' is int/string for categorical axes
        df['Admission_Year'] = df['Admission_Year'].astype(str) 
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(url)

if df.empty:
    st.stop() # Stop the app if data loading failed

# Optional: Display raw data in an expander
with st.expander("View Raw Data"):
    st.dataframe(df)

# --- 2. Visualizations using Plotly Express ---
st.header("Visualizations")

# Re-order Age_Group for consistent plotting (used in the heatmap and others if needed)
age_order = ['18-20', '21-22', '23-24', '25+']
if 'Age_Group' in df.columns:
    df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=age_order, ordered=True)

# Create two columns for the first two charts
col1, col2 = st.columns(2)

## Box Plot: Current CGPA vs. Gender (Plotly Express Box Plot)
with col1:
    st.subheader("1. CGPA Distribution by Gender (Box Plot)")
    
    # Plotly Express Box Plot
    fig1 = px.box(
        df,
        x='Gender',
        y='Current_CGPA',
        title='CGPA Distribution by Gender',
        color='Gender',
        labels={'Current_CGPA': 'Current CGPA', 'Gender': 'Gender'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Set y-axis limits and update layout
    fig1.update_yaxes(range=[2.0, 4.0])
    fig1.update_layout(showlegend=False)
    
    st.plotly_chart(fig1, use_container_width=True)
    

## Violin Plot: CGPA across University Admission Years (Plotly Express Violin Plot)
with col2:
    st.subheader("2. CGPA Distribution across Admission Years (Violin Plot)")
    
    # Plotly Express Violin Plot
    fig2 = px.violin(
        df, 
        x='Admission_Year', 
        y='Current_CGPA', 
        color='Admission_Year',
        box=True, # Add a box plot inside the violin
        points='outliers', # Show outliers
        title='Distribution of Current CGPA across University Admission Years',
        labels={'Current_CGPA': 'Current CGPA', 'Admission_Year': 'University Admission Year'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Set y-axis limits and update layout
    fig2.update_yaxes(range=[2.0, 4.0])
    fig2.update_layout(showlegend=False)
    
    st.plotly_chart(fig2, use_container_width=True)
    

st.markdown("---")

## Heatmap: Average CGPA by Admission Year and Age Group (Plotly Express Heatmap)
st.subheader("3. Average CGPA by Admission Year and Age Group (Heatmap)")

# Calculate the grouped data for the heatmap
heatmap_data_grouped = df.groupby(['Admission_Year', 'Age_Group'])['Current_CGPA'].mean().unstack()

# Reindex columns to ensure correct order
heatmap_data_grouped = heatmap_data_grouped.reindex(columns=age_order)

# Plotly Express Heatmap (px.imshow is often easier for this structure)
fig3 = px.imshow(
    heatmap_data_grouped.values,
    x=heatmap_data_grouped.columns,
    y=heatmap_data_grouped.index,
    color_continuous_scale="YlGnBu",
    text_auto=".2f", # Display text on tiles, formatted to 2 decimal places
    aspect="auto"
)

# Customize layout for the heatmap
fig3.update_layout(
    title='Average CGPA by Admission Year and Age Group',
    xaxis_title='Age Group (Years)',
    yaxis_title='University Admission Year',
    xaxis={'side': 'bottom'} # Move x-axis labels to the bottom
)

# Customize colorbar title
fig3.update_coloraxes(colorbar_title='Average Current CGPA')

st.plotly_chart(fig3, use_container_width=True)


st.markdown("---")

## Grouped Bar Plot: Average CGPA by Income Group and Scholarship (Plotly Express Bar Chart)
st.subheader("4. Average CGPA by Income Group and Meritorious Scholarship")

# Calculate the average CGPA by Income Group and Meritorious Scholarship Status
grouped_data_bar = df.groupby(['Income_Group', 'Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()

# Plotly Express Grouped Bar Chart
fig4 = px.bar(
    grouped_data_bar, 
    x='Income_Group', 
    y='Current_CGPA', 
    color='Meritorious_Scholarship', 
    barmode='group', # Important for grouped bar chart
    title='Average CGPA by Family Income Group and Meritorious Scholarship Status',
    labels={'Current_CGPA': 'Average Current CGPA', 'Income_Group': 'Family Income Group', 'Meritorious_Scholarship': 'Meritorious Scholarship'},
    color_discrete_sequence=px.colors.qualitative.Vivid # Using a different palette
)

# Customize x-axis order if preferred (assuming Income_Group has a natural order)
# fig4.update_xaxes(categoryorder='array', categoryarray=['Low', 'Medium', 'High']) 

st.plotly_chart(fig4, use_container_width=True)

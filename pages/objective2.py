import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. Configuration and Data Loading ---

# You must replace this with your actual data loading method.
# For a reproducible example, this function creates a dummy DataFrame
# with the required columns for demonstration.
@st.cache_data
def load_data():
    """Creates a dummy DataFrame with required columns for demonstration."""
    data = {
        'Daily_Social_Media_Hours': np.random.choice([0, 1, 2, 3, 4, 5], 500),
        'Current_CGPA': np.random.uniform(2.5, 4.0, 500),
        'Attendance_Pct': np.random.uniform(60, 100, 500),
        'Daily_Study_Hours': np.random.choice([0, 1, 2, 3, 4], 500),
        'Learning_Mode': np.random.choice(['Online', 'Physical', 'Hybrid'], 500),
        'Has_PC': np.random.choice(['Yes', 'No'], 500)
    }
    df = pd.DataFrame(data)
    
    # Simulate the effect of study/attendance on CGPA
    df['Current_CGPA'] += (df['Daily_Study_Hours'] * 0.1)
    df['Current_CGPA'] += (df['Attendance_Pct'] / 100 * 0.2)
    df['Current_CGPA'] = df['Current_CGPA'].clip(upper=4.0)
    
    # Ensure categorical columns are treated as categories for ordering
    for col in ['Daily_Social_Media_Hours', 'Daily_Study_Hours']:
        df[col] = df[col].astype('category')
        
    return df

st.title("📊 Interactive Academic Performance Dashboard")
st.markdown("---")

df = load_data()

# --- 2. Box Plot: CGPA vs. Daily Social Media Hours ---
st.header("1. CGPA Distribution by Daily Social Media Hours")

# Plotly Box Plot
# The category_orders parameter is used to ensure the x-axis is ordered numerically
social_media_order = sorted(df['Daily_Social_Media_Hours'].unique().tolist())
fig1 = px.box(
    df,
    x='Daily_Social_Media_Hours',
    y='Current_CGPA',
    title='CGPA Distribution by Daily Social Media Hours',
    color='Daily_Social_Media_Hours', # Add color for distinction
    color_discrete_sequence=px.colors.qualitative.Pastel,
    category_orders={'Daily_Social_Media_Hours': social_media_order}
)
fig1.update_yaxes(range=[2.0, 4.0], autorange=False) # Set y-axis range
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- 3. Scatter Plot: Current CGPA vs. Attendance Percentage (with Correlation) ---
st.header("2. Current CGPA vs. Class Attendance Percentage")

col_scatter, col_corr = st.columns([3, 1])

with col_scatter:
    # Plotly Scatter Plot
    fig2 = px.scatter(
        df,
        x='Attendance_Pct',
        y='Current_CGPA',
        title='Scatter Plot of Current CGPA vs. Class Attendance Percentage',
        labels={
            'Attendance_Pct': 'Class Attendance Percentage (%)',
            'Current_CGPA': 'Current CGPA'
        },
        opacity=0.6,
        trendline='ols', # Add an OLS (linear regression) trendline
        trendline_color_override='red'
    )
    fig2.update_xaxes(range=[0, 100], autorange=False)
    fig2.update_yaxes(range=[2.0, 4.0], autorange=False)
    st.plotly_chart(fig2, use_container_width=True)

with col_corr:
    # Calculate and display the correlation coefficient
    correlation = df['Attendance_Pct'].corr(df['Current_CGPA'])
    st.metric(
        label="Pearson Correlation ($r$)",
        value=f"{correlation:.3f}",
        delta="Relationship Strength"
    )
    st.info(f"A correlation of **{correlation:.3f}** suggests a {'stronger' if abs(correlation) >= 0.5 else 'weaker'} linear relationship.")

st.markdown("---")

# --- 4. Bar Plot: Average CGPA by Daily Study Hours ---
st.header("3. Average CGPA by Daily Study Hours")

# Calculate the average CGPA for each daily study hour category (required for bar plot)
study_hours_data = df.groupby('Daily_Study_Hours')['Current_CGPA'].mean().reset_index()

# Plotly Bar Plot
# The order is maintained by ensuring the 'Daily_Study_Hours' column is categorical/sorted
study_hours_order = sorted(study_hours_data['Daily_Study_Hours'].unique().tolist())
fig3 = px.bar(
    study_hours_data,
    x='Daily_Study_Hours',
    y='Current_CGPA',
    title='Average CGPA by Daily Study Hours',
    labels={'Current_CGPA': 'Average Current CGPA', 'Daily_Study_Hours': 'Daily Study Hours (Hours)'},
    color='Daily_Study_Hours',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    category_orders={'Daily_Study_Hours': study_hours_order}
)
fig3.update_yaxes(range=[study_hours_data['Current_CGPA'].min() - 0.1, 4.0])
fig3.update_layout(showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- 5. Grouped Bar Plot: Average CGPA: PC Ownership vs. Learning Mode ---
st.header("4. Average CGPA: PC Ownership vs. Learning Mode")

# Calculate the average CGPA grouped by both factors
pc_mode_data = df.groupby(['Learning_Mode', 'Has_PC'])['Current_CGPA'].mean().reset_index()

# Plotly Grouped Bar Plot
fig4 = px.bar(
    pc_mode_data,
    x='Learning_Mode',
    y='Current_CGPA',
    color='Has_PC',
    barmode='group', # Key for grouped bar
    title='Average CGPA: PC Ownership vs. Learning Mode',
    labels={
        'Current_CGPA': 'Average Current CGPA',
        'Learning_Mode': 'Preferable Learning Mode',
        'Has_PC': 'Has Personal Computer?'
    },
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig4, use_container_width=True)

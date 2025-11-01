import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set Streamlit page configuration
st.set_page_config(
    page_title="Academic Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

## Data Loading and Preparation
# Define the URL of the CSV file
URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"

@st.cache_data
def load_data():
    """Loads and preprocesses the dataset."""
    try:
        df = pd.read_csv(URL)
        # Ensure Age_Group and Daily_Study_Hours are properly ordered for charts
        age_order = ['18-20', '21-22', '23-24', '25+']
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=age_order, ordered=True)
        
        # Convert Daily_Study_Hours to string categories for proper ordering in plots
        study_hours_order = sorted(df['Daily_Study_Hours'].unique())
        df['Daily_Study_Hours'] = pd.Categorical(df['Daily_Study_Hours'], categories=study_hours_order, ordered=True).astype(str)
        
        # Convert Daily_Social_Media_Hours to string categories for proper ordering in plots
        social_media_order = sorted(df['Daily_Social_Media_Hours'].unique())
        df['Daily_Social_Media_Hours'] = pd.Categorical(df['Daily_Social_Media_Hours'], categories=social_media_order, ordered=True).astype(str)
        
        return df
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

df = load_data()

# Check if data was loaded successfully
if df.empty:
    st.stop()

# --- Streamlit Dashboard Layout ---
st.title("🎓 Academic Performance Analysis Dashboard")

st.sidebar.header("Data Source & Overview")
st.sidebar.markdown(f"Data Loaded Successfully: **{len(df)} records**")

if st.sidebar.checkbox("Show Raw Data", False):
    st.subheader("Raw Data Sample")
    st.dataframe(df.head())

# --- Visualization Functions using Plotly ---

## 1. Box Plot: Current CGPA vs. Gender
def plot_cgpa_vs_gender(data):
    fig = px.box(
        data,
        x='Gender',
        y='Current_CGPA',
        title='CGPA Distribution by Gender',
        color='Gender',
        color_discrete_map={'Male': 'blue', 'Female': 'red'},
        height=450,
        range_y=[2.0, 4.0]
    )
    fig.update_layout(xaxis_title='Gender', yaxis_title='Current CGPA')
    return fig

## 2. Heatmap: Average Current CGPA by Admission Year and Age Group
def plot_cgpa_heatmap(data):
    # Calculate the mean CGPA for each combination
    heatmap_data = data.groupby(['Admission_Year', 'Age_Group'])['Current_CGPA'].mean().unstack()
    
    # Ensure Age_Group categories are ordered correctly
    age_order = ['18-20', '21-22', '23-24', '25+']
    heatmap_data = heatmap_data.reindex(columns=age_order)
    
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index.astype(str),
        color_continuous_scale="YlGnBu",
        aspect="auto",
        text_auto=".2f",
        title='Average CGPA by Admission Year and Age Group'
    )
    fig.update_layout(
        xaxis_title='Age Group (Years)', 
        yaxis_title='University Admission Year',
        height=500
    )
    fig.update_coloraxes(colorbar_title='Average Current CGPA')
    return fig

## 3. Grouped Bar Plot: Average CGPA by Income Group and Meritorious Scholarship Status
def plot_cgpa_by_income_scholarship(data):
    grouped_data = data.groupby(['Income_Group', 'Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    
    fig = px.bar(
        grouped_data,
        x='Income_Group',
        y='Current_CGPA',
        color='Meritorious_Scholarship',
        barmode='group',
        title='Average CGPA by Family Income Group and Meritorious Scholarship Status',
        labels={'Current_CGPA': 'Average Current CGPA', 'Meritorious_Scholarship': 'Meritorious Scholarship?'},
        height=500,
        color_discrete_map={'Yes': 'green', 'No': 'red'}
    )
    fig.update_layout(xaxis_title='Family Income Group', yaxis_title='Average Current CGPA')
    return fig

## 4. Box Plot: CGPA vs. Daily Social Media Hours
def plot_cgpa_vs_social_media(data):
    fig = px.box(
        data,
        x='Daily_Social_Media_Hours',
        y='Current_CGPA',
        title='CGPA Distribution by Daily Social Media Hours',
        color='Daily_Social_Media_Hours',
        height=550,
        range_y=[2.0, 4.0]
    )
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': sorted(data['Daily_Social_Media_Hours'].unique())},
        xaxis_title='Daily Social Media Hours (Hours)', 
        yaxis_title='Current CGPA',
        showlegend=False
    )
    return fig

## 5. Scatter Plot: Current CGPA vs. Attendance Percentage
def plot_cgpa_vs_attendance(data):
    fig = px.scatter(
        data,
        x='Attendance_Pct',
        y='Current_CGPA',
        trendline='ols', # Add a regression line
        title='Scatter Plot of Current CGPA vs. Class Attendance Percentage',
        height=500,
        range_x=[0, 100],
        range_y=[2.0, 4.0]
    )
    
    # Calculate and display the correlation
    correlation = data['Attendance_Pct'].corr(data['Current_CGPA'])
    st.markdown(f"**Correlation between Class Attendance Percentage and Current CGPA:** `{correlation:.2f}`")
    
    fig.update_layout(xaxis_title='Class Attendance Percentage', yaxis_title='Current CGPA')
    return fig

## 6. Bar Plot: Average CGPA by Daily Study Hours
def plot_cgpa_vs_study_hours(data):
    study_hours_data = data.groupby('Daily_Study_Hours')['Current_CGPA'].mean().reset_index()
    
    fig = px.bar(
        study_hours_data,
        x='Daily_Study_Hours',
        y='Current_CGPA',
        color='Daily_Study_Hours',
        title='Average CGPA by Daily Study Hours',
        height=500,
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': sorted(study_hours_data['Daily_Study_Hours'].unique())},
        xaxis_title='Daily Study Hours (Hours)', 
        yaxis_title='Average Current CGPA',
        showlegend=False
    )
    return fig

## 7. Grouped Bar Plot: Average CGPA vs. Has_PC grouped by Learning_Mode
def plot_pc_vs_learning_mode(data):
    pc_mode_data = data.groupby(['Learning_Mode', 'Has_PC'])['Current_CGPA'].mean().reset_index()
    
    fig = px.bar(
        pc_mode_data,
        x='Learning_Mode',
        y='Current_CGPA',
        color='Has_PC',
        barmode='group',
        title='Average CGPA: PC Ownership vs. Learning Mode',
        labels={'Current_CGPA': 'Average Current CGPA', 'Has_PC': 'Has Personal Computer?'},
        height=500,
        color_discrete_map={'Yes': '#E41A1C', 'No': '#377EB8'} # Set1 colors
    )
    fig.update_layout(xaxis_title='Preferable Learning Mode', yaxis_title='Average Current CGPA')
    return fig

## 8. Grouped Box Plot: Current CGPA vs. Fell_Probation grouped by Attends_Consultancy
def plot_probation_consultancy(data):
    fig = px.box(
        data,
        x='Fell_Probation',
        y='Current_CGPA',
        color='Attends_Consultancy',
        title='CGPA Distribution: Probation Status and Teacher Consultancy',
        labels={'Fell_Probation': 'Did you ever fall in probation?', 'Attends_Consultancy': 'Attends Consultancy?'},
        height=500,
        range_y=[2.0, 4.0],
        color_discrete_map={'Yes': 'lightsalmon', 'No': 'skyblue'} # Pastel1 equivalent
    )
    fig.update_layout(xaxis_title='Did you ever fall in probation?', yaxis_title='Current CGPA')
    return fig

## 9. Line Plot: Average Daily Skill Dev Hours vs. Current Semester
def plot_skill_dev_vs_semester(data):
    skill_dev_data = data.groupby('Semester')['Daily_Skill_Dev_Hours'].mean().reset_index()
    
    fig = px.line(
        skill_dev_data,
        x='Semester',
        y='Daily_Skill_Dev_Hours',
        title='Average Daily Skill Development Hours by Current Semester',
        markers=True,
        height=500
    )
    fig.update_layout(
        xaxis_title='Current Semester', 
        yaxis_title='Average Daily Skill Development Hours',
        xaxis={'tickvals': skill_dev_data['Semester'].unique()} # Ensure all semesters are visible
    )
    return fig

## 10. Heatmap (Count): Count of students by English_Proficiency and Fell_Probation
def plot_english_probation_count_heatmap(data):
    # Create a count pivot table
    count_data = data.groupby(['English_Proficiency', 'Fell_Probation']).size().unstack(fill_value=0)
    
    # Reorder English proficiency for logical flow
    english_order = ['Basic', 'Intermediate', 'Advance']
    count_data = count_data.reindex(index=english_order)

    # Convert to Plotly figure
    fig = go.Figure(data=go.Heatmap(
        z=count_data.values,
        x=count_data.columns,
        y=count_data.index,
        colorscale='Reds',
        hoverongaps=False
    ))
    
    # Add annotations (text on heatmap cells)
    annotations = []
    for i, row in enumerate(count_data.index):
        for j, col in enumerate(count_data.columns):
            annotations.append(
                dict(
                    x=col,
                    y=row,
                    text=str(count_data.iloc[i, j]),
                    showarrow=False,
                    font=dict(color="black")
                )
            )
            
    fig.update_layout(
        title='Student Count by English Proficiency and Probation Status',
        xaxis_title='Did you ever fall in probation?',
        yaxis_title='English Language Proficiency',
        annotations=annotations,
        height=500
    )
    fig.update_coloraxes(colorbar_title='Count of Students')
    return fig


# --- Display Charts in Streamlit ---

st.header("1. Core Performance Metrics")
st.markdown("Analyzing CGPA distribution by key demographic factors.")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)

with col2:
    st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)

st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)

st.header("2. Study Habits and CGPA Correlation")
st.markdown("Exploring the relationship between study habits, media consumption, and academic success.")

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(plot_cgpa_vs_study_hours(df), use_container_width=True)

with col4:
    st.plotly_chart(plot_cgpa_vs_social_media(df), use_container_width=True)

st.plotly_chart(plot_cgpa_vs_attendance(df), use_container_width=True)

st.header("3. Environmental and Support Factors")
st.markdown("Investigating the influence of personal equipment, learning mode, and support systems.")

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(plot_pc_vs_learning_mode(df), use_container_width=True)

with col6:
    st.plotly_chart(plot_probation_consultancy(df), use_container_width=True)

st.header("4. Semester Trends and Proficiency")
st.markdown("Examining skill development over semesters and the link between proficiency and probation.")

st.plotly_chart(plot_skill_dev_vs_semester(df), use_container_width=True)
st.plotly_chart(plot_english_probation_count_heatmap(df), use_container_width=True)

st.caption("Dashboard powered by Streamlit and Plotly.")

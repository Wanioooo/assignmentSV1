import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('new_dataset_academic_performance (1).csv')
    df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
    df['Daily_Study_Hours'] = pd.Categorical(df['Daily_Study_Hours'], ordered=True)
    df['Daily_Social_Media_Hours'] = pd.Categorical(df['Daily_Social_Media_Hours'], ordered=True)
    return df

df = load_data()

st.title("Objective 2: Study Habits and Environmental Factors")

# --- Visualization Functions (from main.py) ---

def plot_cgpa_vs_social_media(data):
    fig = px.box(
        data,
        x='Daily_Social_Media_Hours',
        y='Current_CGPA',
        title='CGPA Distribution by Daily Social Media Hours',
        color='Daily_Social_Media_Hours',
        height=550,
        range_y=[2.0,4.0]
    )
    fig.update_layout(
        xaxis={'categoryorder':'array','categoryarray':sorted(data['Daily_Social_Media_Hours'].unique())},
        xaxis_title='Daily Social Media Hours (Hours)',
        yaxis_title='Current CGPA',
        showlegend=False
    )
    return fig

def plot_cgpa_vs_attendance(data):
    fig = px.scatter(
        data,
        x='Attendance_Pct',
        y='Current_CGPA',
        trendline='ols',
        title='Scatter Plot of Current CGPA vs. Class Attendance Percentage',
        height=500,
        range_x=[0,100],
        range_y=[2.0,4.0]
    )
    correlation = data['Attendance_Pct'].corr(data['Current_CGPA'])
    st.markdown(f"**Correlation between Class Attendance Percentage and Current CGPA:** `{correlation:.2f}`")
    fig.update_layout(xaxis_title='Class Attendance Percentage', yaxis_title='Current CGPA')
    return fig

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
        xaxis={'categoryorder':'array','categoryarray':sorted(study_hours_data['Daily_Study_Hours'].unique())},
        xaxis_title='Daily Study Hours (Hours)',
        yaxis_title='Average Current CGPA',
        showlegend=False
    )
    return fig

def plot_pc_vs_learning_mode(data):
    pc_mode_data = data.groupby(['Learning_Mode','Has_PC'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        pc_mode_data,
        x='Learning_Mode',
        y='Current_CGPA',
        color='Has_PC',
        barmode='group',
        title='Average CGPA: PC Ownership vs. Learning Mode',
        labels={'Current_CGPA':'Average Current CGPA','Has_PC':'Has Personal Computer?'},
        height=500,
        color_discrete_map={'Yes':'#E41A1C','No':'#377EB8'}
    )
    fig.update_layout(xaxis_title='Preferable Learning Mode', yaxis_title='Average Current CGPA')
    return fig

# --- Display Visualizations ---
st.plotly_chart(plot_cgpa_vs_social_media(df), width='stretch')
st.plotly_chart(plot_cgpa_vs_attendance(df), width='stretch')
st.plotly_chart(plot_cgpa_vs_study_hours(df), width='stretch')
st.plotly_chart(plot_pc_vs_learning_mode(df), width='stretch')

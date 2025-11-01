# objective3.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def vis8(df):
    fig = px.box(df, x='Fell_Probation', y='Current_CGPA', color='Attends_Consultancy',
                 title='CGPA vs Probation & Consultancy')
    st.plotly_chart(fig, width="stretch")

def vis9(df):
    fig = px.line(df.groupby('Semester')['Daily_Skill_Dev_Hours'].mean().reset_index(),
                  x='Semester', y='Daily_Skill_Dev_Hours', markers=True,
                  title='Average Daily Skill Development Hours by Semester')
    st.plotly_chart(fig, width="stretch")

def vis10(df):
    count_data = df.groupby(['English_Proficiency','Fell_Probation']).size().unstack(fill_value=0)
    fig = go.Figure(data=go.Heatmap(z=count_data.values, x=count_data.columns, y=count_data.index))
    fig.update_layout(title='English Proficiency vs Probation Count')
    st.plotly_chart(fig, width="stretch")

def run_objective3():
    st.title("Objective 3: Academic Support & Proficiency")
    df = pd.read_csv("new_dataset_academic_performance (1).csv")
    vis8(df)
    vis9(df)
    vis10(df)


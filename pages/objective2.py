# objective2.py
import streamlit as st
import pandas as pd
import plotly.express as px

def vis4(df):
    fig = px.bar(df.groupby('Daily_Study_Hours')['Current_CGPA'].mean().reset_index(),
                 x='Daily_Study_Hours', y='Current_CGPA', title='Average CGPA by Study Hours')
    st.plotly_chart(fig, width="stretch")

def vis5(df):
    fig = px.box(df, x='Daily_Social_Media_Hours', y='Current_CGPA', title='CGPA vs Social Media Hours')
    st.plotly_chart(fig, width="stretch")

def vis6(df):
    fig = px.scatter(df, x='Attendance_Pct', y='Current_CGPA', trendline='ols',
                     title='CGPA vs Attendance')
    st.plotly_chart(fig, width="stretch")

def vis7(df):
    grouped = df.groupby(['Learning_Mode','Has_PC'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(grouped, x='Learning_Mode', y='Current_CGPA', color='Has_PC', barmode='group',
                 title='Average CGPA: PC Ownership vs Learning Mode')
    st.plotly_chart(fig, width="stretch")

def run_objective2():
    st.title("Objective 2: Study Habits & Environmental Factors")
    df = pd.read_csv("new_dataset_academic_performance (1).csv")
    vis4(df)
    vis5(df)
    vis6(df)
    vis7(df)

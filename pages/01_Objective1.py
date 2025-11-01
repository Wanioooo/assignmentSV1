# objective1.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('new_dataset_academic_performance (1).csv')
    return df

df = load_data()

def vis1(df):
    fig = px.box(df, x='Gender', y='Current_CGPA', title='CGPA vs Gender')
    st.plotly_chart(fig, width="stretch")

def vis2(df):
    heatmap_data = df.groupby(['Admission_Year','Age_Group'])['Current_CGPA'].mean().unstack()
    fig = px.imshow(heatmap_data, text_auto=".2f", title='Average CGPA by Admission Year & Age Group')
    st.plotly_chart(fig, width="stretch")

def vis3(df):
    grouped = df.groupby(['Income_Group','Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(grouped, x='Income_Group', y='Current_CGPA', color='Meritorious_Scholarship', barmode='group')
    st.plotly_chart(fig, width="stretch")

def run_objective1():
    st.title("Objective 1: Core Performance Metrics")
    df = pd.read_csv("new_dataset_academic_performance (1).csv")
    vis1(df)
    vis2(df)
    vis3(df)

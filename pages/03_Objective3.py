import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('new_dataset_academic_performance (1).csv')
    df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
    return df

df = load_data()

st.title("Objective 3: Support Systems and Skill Development")

# --- Visualization Functions (from main.py) ---

def plot_probation_consultancy(data):
    fig = px.box(
        data,
        x='Fell_Probation',
        y='Current_CGPA',
        color='Attends_Consultancy',
        title='CGPA Distribution: Probation Status and Teacher Consultancy',
        labels={'Fell_Probation':'Did you ever fall in probation?','Attends_Consultancy':'Attends Consultancy?'},
        height=500,
        range_y=[2.0,4.0],
        color_discrete_map={'Yes':'lightsalmon','No':'skyblue'}
    )
    fig.update_layout(xaxis_title='Did you ever fall in probation?', yaxis_title='Current CGPA')
    return fig

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
        xaxis={'tickvals':skill_dev_data['Semester'].unique()}
    )
    return fig

def plot_english_probation_count_heatmap(data):
    count_data = data.groupby(['English_Proficiency','Fell_Probation']).size().unstack(fill_value=0)
    english_order = ['Basic','Intermediate','Advance']
    count_data = count_data.reindex(index=english_order)
    fig = go.Figure(data=go.Heatmap(
        z=count_data.values,
        x=count_data.columns,
        y=count_data.index,
        colorscale='Reds',
        hoverongaps=False
    ))
    annotations = []
    for i,row in enumerate(count_data.index):
        for j,col in enumerate(count_data.columns):
            annotations.append(dict(
                x=col,
                y=row,
                text=str(count_data.iloc[i,j]),
                showarrow=False,
                font=dict(color="black")
            ))
    fig.update_layout(
        title='Student Count by English Proficiency and Probation Status',
        xaxis_title='Did you ever fall in probation?',
        yaxis_title='English Language Proficiency',
        annotations=annotations,
        height=500
    )
    fig.update_coloraxes(colorbar_title='Count of Students')
    return fig

# --- Display Visualizations ---
st.plotly_chart(plot_probation_consultancy(df), width='stretch')
st.plotly_chart(plot_skill_dev_vs_semester(df), width='stretch')
st.plotly_chart(plot_english_probation_count_heatmap(df), width='stretch')

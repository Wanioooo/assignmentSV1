import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('new_dataset_academic_performance (1).csv')
    # Optional: make sure categories are ordered as in main.py
    df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
    return df

df = load_data()

st.header("Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("🎓 Analyze the influence of socio-economic and demographic factors on student academic performance (Current CGPA). ")

# --- Visualization Functions from main.py ---

st.subheader("Visualization 1: Box Plot of CGPA Distribution by Gender")

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

st.subheader("Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")

def plot_cgpa_heatmap(data):
    heatmap_data = data.groupby(['Admission_Year','Age_Group'])['Current_CGPA'].mean().unstack()
    age_order = ['18-20','21-22','23-24','25+']
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
    fig.update_layout(xaxis_title='Age Group (Years)', yaxis_title='University Admission Year', height=500)
    fig.update_coloraxes(colorbar_title='Average Current CGPA')
    return fig
    
st.subheader("Visualization 3: Group Bar Plot Average CGPA by Family Income Group and Meritorious Scholarship Status.")

def plot_cgpa_by_income_scholarship(data):
    grouped_data = data.groupby(['Income_Group','Meritorious_Scholarship'])['Current_CGPA'].mean().reset_index()
    fig = px.bar(
        grouped_data,
        x='Income_Group',
        y='Current_CGPA',
        color='Meritorious_Scholarship',
        barmode='group',
        title='Average CGPA by Family Income Group and Meritorious Scholarship Status',
        labels={'Current_CGPA':'Average Current CGPA','Meritorious_Scholarship':'Meritorious Scholarship?'},
        height=500,
        color_discrete_map={'Yes':'green','No':'red'}
    )
    fig.update_layout(xaxis_title='Family Income Group', yaxis_title='Average Current CGPA')
    return fig

# --- Display the 3 visualizations ---
st.plotly_chart(plot_cgpa_vs_gender(df), width='stretch')
st.plotly_chart(plot_cgpa_heatmap(df), width='stretch')
st.plotly_chart(plot_cgpa_by_income_scholarship(df), width='stretch')

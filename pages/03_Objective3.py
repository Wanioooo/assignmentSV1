import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration for better layout
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('new_dataset_academic_performance (1).csv')
        
        # Ensure categories are ordered
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        english_order = ['Basic', 'Intermediate', 'Advance']
        df['English_Proficiency'] = pd.Categorical(df['English_Proficiency'], categories=english_order, ordered=True)
        
        return df
    except FileNotFoundError:
        st.error("🚨 Error: Data file 'new_dataset_academic_performance (1).csv' not found. Please ensure it is in the correct path.")
        return pd.DataFrame({
            'Current_CGPA': [], 'Fell_Probation': [], 'Attends_Consultancy': [], 
            'Semester': [], 'Daily_Skill_Dev_Hours': [], 'English_Proficiency': []
        })
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred during data loading: {e}")
        return pd.DataFrame({
            'Current_CGPA': [], 'Fell_Probation': [], 'Attends_Consultancy': [], 
            'Semester': [], 'Daily_Skill_Dev_Hours': [], 'English_Proficiency': []
        })

df = load_data()

st.title("Objective 3: Academic Challenges and Student Engagement")
st.markdown("🤝 Explore the interplay of academic challenges and student engagement with overall performance.")

# Check if data is valid
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    pass
else:
    # --- START: Key Metric Summary Section ---
    st.header("Key Support and Skill Metrics", divider="green")

    col_p, col_c, col_s = st.columns(3)

    probation_rate = (df['Fell_Probation'].astype(str).str.lower() == 'yes').mean() * 100
    col_p.metric(
        "Overall Probation Rate",
        f"{probation_rate:.1f}%",
        help="Percentage of students who have reported falling on academic probation."
    )

    consultancy_cgpa = df.groupby('Attends_Consultancy')['Current_CGPA'].mean()
    consultancy_yes = consultancy_cgpa.get('Yes', 0)
    consultancy_no = consultancy_cgpa.get('No', 0)
    cgpa_diff = consultancy_yes - consultancy_no

    col_c.metric(
        "Consultancy CGPA Boost",
        f"{cgpa_diff:.2f}",
        delta_color="normal",
        delta="Higher CGPA" if cgpa_diff > 0 else "Lower CGPA",
        help=f"Avg CGPA of students who attend consultancy ({consultancy_yes:.2f}) vs. those who don't ({consultancy_no:.2f})."
    )

    avg_skill_dev = df['Daily_Skill_Dev_Hours'].mean()
    col_s.metric(
        "Avg. Daily Skill Dev. Hours",
        f"{avg_skill_dev:.1f} hrs",
        help="Average time spent daily by students on skill development."
    )

    st.subheader("English Proficiency & Probation Rates")

    english_prob_rates = df.groupby('English_Proficiency')['Fell_Probation'].apply(
        lambda x: (x.astype(str).str.lower() == 'yes').mean()) * 100

    col_basic, col_inter, col_adv = st.columns(3)
    col_basic.info(f"*Basic English Probation Rate:* {english_prob_rates.get('Basic', 0):.1f}%")
    col_inter.info(f"*Intermediate English Probation Rate:* {english_prob_rates.get('Intermediate', 0):.1f}%")
    col_adv.info(f"*Advanced English Probation Rate:* {english_prob_rates.get('Advance', 0):.1f}%")

    st.divider()

# --- Visualization Functions ---
def plot_probation_consultancy(data):
    fig = px.box(
        data,
        x='Fell_Probation',
        y='Current_CGPA',
        color='Attends_Consultancy',
        title='Visualization 1: CGPA Distribution: Probation Status and Teacher Consultancy',
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
        title='Visualization 2: Average Daily Skill Development Hours by Current Semester',
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
        title='Visualization 3: Student Count by English Proficiency and Probation Status',
        xaxis_title='Did you ever fall in probation?',
        yaxis_title='English Language Proficiency',
        annotations=annotations,
        height=500
    )
    fig.update_coloraxes(colorbar_title='Count of Students')
    return fig

# --- Summary Box before visualization ---
st.header("Summary Box: Academic Challenges and Student Engagement", divider="red")
with st.container(border=True):
    st.markdown("""
    *Summary:*
    This objective explores how academic challenges (probation, language proficiency) and engagement (consultancy attendance, skill development) interact to affect student performance.
    Students who attend **teacher consultancy sessions** tend to have **higher CGPA**, suggesting that support-seeking behavior contributes to improved outcomes.
    Meanwhile, **English proficiency** correlates strongly with lower probation rates, emphasizing communication skills as a key success factor.
    Additionally, **skill development efforts** increase as students progress through semesters, showing growing awareness of employability and academic maturity.
    """)

# --- Display Visualizations with Interpretation ---
st.subheader("Visualization 1: CGPA Distribution: Probation Status and Teacher Consultancy")
st.plotly_chart(plot_probation_consultancy(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
Students who have never fallen on probation consistently show higher CGPA, and this performance gap widens among those who attend teacher consultancy.
This suggests that proactive engagement with faculty provides academic stability, particularly for at-risk students who might otherwise face performance decline.
""")

st.subheader("Visualization 2: Average Daily Skill Development Hours by Current Semester")
st.plotly_chart(plot_skill_dev_vs_semester(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
A gradual increase in average skill development hours across semesters indicates that students invest more time in personal and technical growth as they advance in their academic journey.
This trend may reflect awareness of future career readiness and practical skill acquisition in higher semesters.
""")

st.subheader("Visualization 3: Student Count by English Proficiency and Probation Status")
st.plotly_chart(plot_english_probation_count_heatmap(df), use_container_width=True)
st.markdown("""
**Interpretation:**  
Students with *Basic English proficiency* show a notably higher probation count compared to *Intermediate* and *Advanced* groups.
This pattern demonstrates that language ability plays a crucial role in academic retention and performance, reinforcing the need

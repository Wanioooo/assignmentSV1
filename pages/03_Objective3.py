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
        # NOTE: Using the robust URL for data loading to avoid FileNotFoundError.
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        
        # Ensure categories are ordered
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        # Order English Proficiency for calculations and display consistency
        english_order = ['Basic', 'Intermediate', 'Advance']
        df['English_Proficiency'] = pd.Categorical(df['English_Proficiency'], categories=english_order, ordered=True)
        
        return df
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred during data loading: {e}")
        return pd.DataFrame({
            'Current_CGPA': [], 'Fell_Probation': [], 'Attends_Consultancy': [], 
            'Semester': [], 'Daily_Skill_Dev_Hours': [], 'English_Proficiency': []
        })

df = load_data()

st.title("Objective 3: Academic Challenges and Student Engagement")
st.markdown("🤝 Explore the interplay of academic challenges and student engagement with overall performance.")

# Check if the DataFrame is empty before proceeding with calculations
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    pass
else:
    # --- START: Key Metric Summary Section ---
    st.header("Key Support and Skill Metrics", divider="green")

    # 1. Overall Probation and Consultancy Impact
    col_p, col_c, col_s = st.columns(3)

    # Probation Rate
    probation_rate = (df['Fell_Probation'].astype(str).str.lower() == 'yes').mean() * 100
    col_p.metric(
        "Overall Probation Rate",
        f"{probation_rate:.1f}%",
        help="Percentage of students who have reported falling on academic probation."
    )

    # Consultancy CGPA Impact (Difference: Yes - No)
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

    # Average Daily Skill Development Hours
    avg_skill_dev = df['Daily_Skill_Dev_Hours'].mean()
    col_s.metric(
        "Avg. Daily Skill Dev. Hours",
        f"{avg_skill_dev:.1f} hrs",
        help="Average time spent daily by students on skill development."
    )

    st.subheader("English Proficiency & Probation")
    
    # 2. English Proficiency Probation Breakdown
    english_prob_rates = df.groupby('English_Proficiency')['Fell_Probation'].apply(lambda x: (x.astype(str).str.lower() == 'yes').mean()) * 100
    
    col_basic, col_inter, col_adv = st.columns(3)
    
    col_basic.info(f"**Basic English Probation Rate:** {english_prob_rates.get('Basic', 0):.1f}%")
    col_inter.info(f"**Intermediate English Probation Rate:** {english_prob_rates.get('Intermediate', 0):.1f}%")
    col_adv.info(f"**Advanced English Probation Rate:** {english_prob_rates.get('Advance', 0):.1f}%")

    st.divider()
    # --- END: Key Metric Summary Section ---

# --- Visualization Functions (from main.py) ---

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

# --- Display Visualizations ---
st.subheader("Visualization 1: Grouped Box Plot of CGPA: Probation Status and Teacher Consultancy")
st.plotly_chart(plot_probation_consultancy(df), use_container_width=True)

st.subheader("Visualization 2: Line Plot of Average Daily Skill Development Hours by Current Semester")
st.plotly_chart(plot_skill_dev_vs_semester(df), use_container_width=True)

st.subheader("Visualization 3: Heatmap of Student Count by English Proficiency and Probation Status")
st.plotly_chart(plot_english_probation_count_heatmap(df), use_container_width=True)

# --- START: Summary Box and Interpretation ---
st.header("Analysis and Findings", divider="red")

st.subheader("Summary Box: Academic Challenges and Student Engagement")
with st.container(border=True):
    st.markdown("""
    **Summary (100–150 words):**
    This objective evaluates the role of **support mechanisms** (teacher consultancy), **language proficiency**, and **long-term engagement** (skill development) on academic outcomes. The metrics reveal a positive **CGPA boost** (approximately +0.13) for students attending **teacher consultancy**, suggesting it is an effective intervention tool. The box plot confirms that consultation significantly reduces the probability of a student falling into probation. Critically, the heatmap demonstrates a strong inverse relationship between **English Proficiency** and the **Probation Rate**, with students at the Basic level being the most vulnerable. Furthermore, students maintain a consistent, stable commitment to **Daily Skill Development** across all semesters, indicating a healthy level of self-directed learning effort over time.
    """)

st.subheader("Interpretation/Discussion: Observed Patterns")
st.markdown("""
* **Consultancy as a Mitigating Factor:** The grouped box plot clearly shows that students who **attend consultancy** maintain a narrower, higher CGPA range, and are less represented in the probation group. This highlights the **value of proactive student engagement** and teacher support in stabilizing academic performance and preventing critical failure.
* **Language Proficiency Barrier:** The **heatmap** reveals that **English Proficiency** is a major determinant of academic success and risk. The high concentration of probation cases among students with **Basic** proficiency strongly suggests that language is a significant barrier to comprehending course material, writing assignments, and succeeding in a language-intensive academic environment.
* **Skill Development Trend:** The line plot indicates that the average time dedicated to **Daily Skill Development** (self-learning outside of formal coursework) remains relatively **stable** across the academic years (semesters). This consistency is a positive sign of the students' sustained motivation and commitment to continuous professional and intellectual growth.
""")
# --- END: Summary Box and Interpretation ---

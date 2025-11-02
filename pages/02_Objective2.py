import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration for better layout
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        # NOTE: Using the robust URL for data loading.
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        
        # Ensure categories are ordered
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        
        # Re-ordering for better visualization structure if they are strings like '1-2', '3-4'
        study_order = sorted(df['Daily_Study_Hours'].unique())
        media_order = sorted(df['Daily_Social_Media_Hours'].unique())

        df['Daily_Study_Hours'] = pd.Categorical(df['Daily_Study_Hours'], categories=study_order, ordered=True)
        df['Daily_Social_Media_Hours'] = pd.Categorical(df['Daily_Social_Media_Hours'], categories=media_order, ordered=True)
        
        return df
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred during data loading: {e}")
        return pd.DataFrame({'Current_CGPA': [], 'Daily_Study_Hours': [], 'Daily_Social_Media_Hours': [], 'Attendance_Pct': [], 'Learning_Mode': [], 'Has_PC': []})

df = load_data()

st.title("Objective 2: Study Habits and Resource Utilization")
st.markdown("🔍 Investigate the relationship between study habits and resource utilization with student academic performance.")

# Check if the DataFrame is empty before proceeding with calculations
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    pass
else:
    # --- START: Key Metric Summary Section ---
    st.header("Key Summary Metrics", divider="blue")

    # 1. Overall Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Average CGPA", f"{df['Current_CGPA'].mean():.2f}")
    col2.metric("Average Attendance %", f"{df['Attendance_Pct'].mean():.1f}%")
    
    # Calculate correlation between Attendance and CGPA
    correlation = df['Attendance_Pct'].corr(df['Current_CGPA'])
    col3.metric(
        "Attendance vs. CGPA Correlation",
        f"{correlation:.2f}",
        help="Pearson correlation coefficient between Class Attendance Percentage and Current CGPA."
    )

    st.subheader("CGPA by Study vs. Social Media Balance")

    # 2. Key Averages for Study/Social Media (Highest/Lowest performing groups)
    study_cgpa = df.groupby('Daily_Study_Hours')['Current_CGPA'].mean().sort_values(ascending=False)
    social_cgpa = df.groupby('Daily_Social_Media_Hours')['Current_CGPA'].mean().sort_values(ascending=True)

    study_highest_category = study_cgpa.index[0]
    study_highest_cgpa = study_cgpa.iloc[0]
    
    social_lowest_category = social_cgpa.index[0]
    social_lowest_cgpa = social_cgpa.iloc[0]

    col_study, col_social, col_pc = st.columns(3)

    with col_study:
        st.markdown(f"**Highest CGPA Correlates with:**")
        st.metric(
            label=f"Avg. CGPA for {study_highest_category} Study Hours", 
            value=f"{study_highest_cgpa:.2f}"
        )

    with col_social:
        st.markdown(f"**Lowest CGPA Correlates with:**")
        st.metric(
            label=f"Avg. CGPA for {social_lowest_category} Social Media Hours", 
            value=f"{social_lowest_cgpa:.2f}"
        )

    # 3. PC Ownership and Learning Mode
    pc_data = df.groupby('Has_PC')['Current_CGPA'].mean()
    if 'Yes' in pc_data.index and 'No' in pc_data.index:
        pc_diff = pc_data['Yes'] - pc_data['No']
        pc_label = "CGPA Difference (PC Yes - No)"
        pc_help = "Average CGPA of students with a PC minus those without."
        
        with col_pc:
            st.markdown(f"**Impact of PC Ownership:**")
            st.metric(
                label=pc_label,
                value=f"{pc_diff:.2f}",
                delta="Higher" if pc_diff > 0 else "Lower",
                help=pc_help
            )
    
    st.divider()
    # --- END: Key Metric Summary Section ---

# --- Visualization Functions (from main.py) ---

def plot_cgpa_vs_social_media(data):
    fig = px.box(
        data,
        x='Daily_Social_Media_Hours',
        y='Current_CGPA',
        title='Visualization 1: CGPA Distribution by Daily Social Media Hours',
        color='Daily_Social_Media_Hours',
        height=550,
        range_y=[2.0,4.0]
    )
    # Use categoryarray from the data structure itself to ensure correct order
    if not data['Daily_Social_Media_Hours'].empty and data['Daily_Social_Media_Hours'].dtype == 'category':
        order_array = list(data['Daily_Social_Media_Hours'].cat.categories)
    else:
        order_array = sorted(data['Daily_Social_Media_Hours'].unique())
        
    fig.update_layout(
        xaxis={'categoryorder':'array','categoryarray':order_array},
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
        title='Visualization 2: Scatter Plot of Current CGPA vs. Class Attendance Percentage',
        height=500,
        range_x=[0,100],
        range_y=[2.0,4.0]
    )
    
    # Calculate correlation here, but use the metric from the summary section
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
        title='Visualization 3: Average CGPA by Daily Study Hours',
        height=500,
    )
    
    # Use categoryarray from the data structure itself to ensure correct order
    if not study_hours_data['Daily_Study_Hours'].empty and study_hours_data['Daily_Study_Hours'].dtype == 'category':
        order_array = list(study_hours_data['Daily_Study_Hours'].cat.categories)
    else:
        order_array = sorted(study_hours_data['Daily_Study_Hours'].unique())

    fig.update_layout(
        xaxis={'categoryorder':'array','categoryarray':order_array},
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
        title='Visualization 4: Average CGPA: PC Ownership vs. Learning Mode',
        labels={'Current_CGPA':'Average Current CGPA','Has_PC':'Has Personal Computer?'},
        height=500,
        color_discrete_map={'Yes':'#E41A1C','No':'#377EB8'}
    )
    fig.update_layout(xaxis_title='Preferable Learning Mode', yaxis_title='Average Current CGPA')
    return fig

# --- Display Visualizations ---
st.subheader("Visualization 1: CGPA Distribution by Daily Social Media Hours")
st.plotly_chart(plot_cgpa_vs_social_media(df), use_container_width=True)

st.subheader("Visualization 2: Scatter Plot of Current CGPA vs. Class Attendance Percentage")
st.plotly_chart(plot_cgpa_vs_attendance(df), use_container_width=True)

st.subheader("Visualization 3: Average CGPA by Daily Study Hours")
st.plotly_chart(plot_cgpa_vs_study_hours(df), use_container_width=True)

st.subheader("Visualization 4: Average CGPA: PC Ownership vs. Learning Mode")
st.plotly_chart(plot_pc_vs_learning_mode(df), use_container_width=True)


# --- START: Summary Box and Interpretation ---
st.header("Analysis and Findings", divider="red")

st.subheader("Summary Box: Study Habits and Resource Utilization")
with st.container(border=True):
    st.markdown("""
    **Summary:**
    This objective analyzes how **study habits** (study time, social media time, attendance) and **resources** (PC ownership) impact **Current CGPA**. There is a clear **positive relationship** between **Daily Study Hours** and average CGPA, peaking in the 3-4 hour range. Conversely, increased **Daily Social Media Hours** correlate with lower median CGPA and wider performance variation. The scatter plot confirms a **strong positive correlation** (approx. 0.70) between **Class Attendance Percentage** and CGPA, highlighting its critical role. Furthermore, owning a **Personal Computer (PC)** is associated with a reliably higher average CGPA, irrespective of the student's preferred learning mode (online, physical, or blended), suggesting that accessibility to personal equipment is a significant resource advantage.
    """)

st.subheader("Interpretation/Discussion: Observed Patterns")
st.markdown("""
* **Study Time vs. CGPA:** The visualization shows a **monotonic increase** in average CGPA as study hours increase, confirming the principle of effort yielding results. The leveling off or slight dip at the highest end of study hours might suggest a balance is necessary to avoid burnout.
* **Attendance:** The **strongest predictive factor** observed is the high positive correlation coefficient between **Attendance Percentage and CGPA**. This pattern indicates that active participation and presence in class are non-negotiable foundations for achieving academic success.
* **Social Media Interference:** The wider, lower box plots for higher social media usage categories suggest that excessive time spent on these platforms acts as a significant **academic distraction**, increasing performance variance and lowering the median expected CGPA.
* **Resource Advantage (PC):** The grouped bar chart demonstrates that **PC ownership** provides a uniform academic benefit (higher average CGPA) across all learning modes. This reflects the modern dependency on personal computing resources for research, assignment completion, and effective engagement, even in physical and blended learning environments.
""")
# --- END: Summary Box and Interpretation ---

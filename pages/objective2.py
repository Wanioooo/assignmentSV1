# pages/objective2.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def make_demo_data(n=500):
    """Create dummy dataset for Objective 2 (used for testing / layout)."""
    data = {
        'Daily_Social_Media_Hours': np.random.choice([0, 1, 2, 3, 4, 5], n),
        'Current_CGPA': np.random.uniform(2.5, 4.0, n),
        'Attendance_Pct': np.random.uniform(60, 100, n),
        'Daily_Study_Hours': np.random.choice([0, 1, 2, 3, 4], n),
        'Learning_Mode': np.random.choice(['Online', 'Physical', 'Hybrid'], n),
        'Has_PC': np.random.choice(['Yes', 'No'], n)
    }
    df = pd.DataFrame(data)

    # Simulate influence of study/attendance on CGPA
    df['Current_CGPA'] += (df['Daily_Study_Hours'] * 0.1)
    df['Current_CGPA'] += (df['Attendance_Pct'] / 100 * 0.2)
    df['Current_CGPA'] = df['Current_CGPA'].clip(upper=4.0)

    # Make some columns categorical for ordered plotting
    df['Daily_Social_Media_Hours'] = df['Daily_Social_Media_Hours'].astype('category')
    df['Daily_Study_Hours'] = df['Daily_Study_Hours'].astype('category')
    return df

def run_objective2():
    """Entry point for the Objective 2 page."""
    st.title("📚 Objective 2: Learning Factors")
    st.write("Interactive analyses exploring the relationship between study habits, attendance and CGPA.")
    st.markdown("---")

    # Attempt to load real CSV first (optional). If not found, fallback to demo data.
    try:
        # Change this path to the GitHub raw url or local CSV if you want the real data
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        st.success("Loaded dataset from GitHub.")
    except Exception:
        st.warning("Could not load CSV from GitHub — using demo data.")
        df = make_demo_data()

    # ----------------------
    # 1) Box: CGPA vs Social Media Hours
    # ----------------------
    st.header("1. CGPA Distribution by Daily Social Media Hours")
    social_media_order = sorted(df['Daily_Social_Media_Hours'].unique().tolist())
    fig1 = px.box(
        df,
        x='Daily_Social_Media_Hours',
        y='Current_CGPA',
        title='CGPA Distribution by Daily Social Media Hours',
        color='Daily_Social_Media_Hours',
        category_orders={'Daily_Social_Media_Hours': social_media_order},
    )
    fig1.update_yaxes(range=[2.0, 4.0], autorange=False)
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # ----------------------
    # 2) Scatter: Attendance vs CGPA + correlation
    # ----------------------
    st.header("2. Current CGPA vs. Class Attendance Percentage")
    col_scatter, col_corr = st.columns([3, 1])

    with col_scatter:
        fig2 = px.scatter(
            df,
            x='Attendance_Pct',
            y='Current_CGPA',
            title='Attendance vs Current CGPA',
            opacity=0.6,
            trendline='ols'
        )
        fig2.update_xaxes(range=[0, 100], autorange=False)
        fig2.update_yaxes(range=[2.0, 4.0], autorange=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col_corr:
        correlation = df['Attendance_Pct'].corr(df['Current_CGPA'])
        st.metric(label="Pearson r", value=f"{correlation:.3f}")
        st.info(f"A correlation of **{correlation:.3f}** suggests a "
                f"{'strong' if abs(correlation) >= 0.5 else 'moderate/weak'} linear relationship.")

    st.markdown("---")

    # ----------------------
    # 3) Bar: Average CGPA by Study Hours
    # ----------------------
    st.header("3. Average CGPA by Daily Study Hours")
    study_hours_data = df.groupby('Daily_Study_Hours', as_index=False)['Current_CGPA'].mean()
    study_hours_order = sorted(study_hours_data['Daily_Study_Hours'].astype(str).unique().tolist())
    fig3 = px.bar(
        study_hours_data,
        x='Daily_Study_Hours',
        y='Current_CGPA',
        title='Average CGPA by Daily Study Hours',
        category_orders={'Daily_Study_Hours': study_hours_order}
    )
    fig3.update_yaxes(range=[study_hours_data['Current_CGPA'].min() - 0.1, 4.0])
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ----------------------
    # 4) Grouped Bar: Learning Mode vs Has_PC
    # ----------------------
    st.header("4. Average CGPA: PC Ownership vs. Learning Mode")
    pc_mode = df.groupby(['Learning_Mode', 'Has_PC'], as_index=False)['Current_CGPA'].mean()
    fig4 = px.bar(
        pc_mode,
        x='Learning_Mode',
        y='Current_CGPA',
        color='Has_PC',
        barmode='group',
        title='Average CGPA: PC Ownership vs. Learning Mode'
    )
    st.plotly_chart(fig4, use_container_width=True)

# Allow running the page directly (for testing)
if __name__ == "__main__":
    run_objective2()

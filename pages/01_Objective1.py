import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration for better layout (optional, but good practice)
st.set_page_config(layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        # NOTE: Using the provided URL for robustness, as local file path errors are common.
        URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV1/refs/heads/main/new_dataset_academic_performance%20(1).csv"
        df = pd.read_csv(URL)
        
        # Optional: make sure categories are ordered
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=['18-20','21-22','23-24','25+'], ordered=True)
        
        # Ensure Income_Group is a string for plotting consistency
        df['Income_Group'] = df['Income_Group'].astype(str)
        
        return df
    except Exception as e:
        # Catch any error, including file not found for the URL
        st.error(f"🚨 An error occurred during data loading from URL: {e}")
        # Return an empty DataFrame to prevent NameError in the rest of the script
        return pd.DataFrame({'Current_CGPA': [], 'Gender': [], 'Admission_Year': [], 'Age_Group': [], 'Income_Group': [], 'Meritorious_Scholarship': []})

df = load_data()

# Check if the DataFrame is empty before proceeding with calculations
if df.empty or 'Current_CGPA' not in df.columns:
    st.warning("Cannot run analysis: Data is either empty or failed to load correctly.")
    st.stop() # Stop execution if data is invalid

# --- App Content Starts Here ---

st.header("Objective 1: Socio-economic and Demographic Influence", divider="gray")
st.markdown("🎓 Analyze the influence of socio-economic and demographic factors on student academic performance (Current CGPA). ")

# --- START: Summary Metrics Section ---
st.subheader("Key Summary Metrics for Academic Performance")

# 1. Overall CGPA Metrics
avg_cgpa = df['Current_CGPA'].mean()
median_cgpa = df['Current_CGPA'].median()
std_cgpa = df['Current_CGPA'].std()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Current CGPA (Overall)", value=f"{avg_cgpa:.2f}")

with col2:
    st.metric(label="Median Current CGPA (Overall)", value=f"{median_cgpa:.2f}")

with col3:
    st.metric(label="Std. Dev. of Current CGPA", value=f"{std_cgpa:.2f}")

st.divider()

# 2. Gender-Specific Metrics
st.subheader("Average CGPA by Gender")
gender_cgpa = df.groupby('Gender')['Current_CGPA'].mean().reset_index()

col_m, col_f = st.columns(2)

# Safely extract male and female averages
male_avg = gender_cgpa[gender_cgpa['Gender'] == 'Male']['Current_CGPA'].iloc[0] if 'Male' in gender_cgpa['Gender'].values else 0.00
female_avg = gender_cgpa[gender_cgpa['Gender'] == 'Female']['Current_CGPA'].iloc[0] if 'Female' in gender_cgpa['Gender'].values else 0.00

with col_m:
    st.info(f"*Male Average CGPA:* {male_avg:.2f}")

with col_f:
    st.info(f"*Female Average CGPA:* {female_avg:.2f}")
    
st.divider()
# --- END: Summary Metrics Section ---


# --- Visualization Functions ---

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
st.subheader("Visualization 1: Box Plot of CGPA Distribution by Gender")
st.plotly_chart(plot_cgpa_vs_gender(df), use_container_width=True)

st.subheader("Visualization 2: Heatmap of Average CGPA by Admission Year and Age Group")
st.plotly_chart(plot_cgpa_heatmap(df), use_container_width=True)

st.subheader("Visualization 3: Group Bar Plot Average CGPA by Family Income Group and Meritorious Scholarship Status.")
st.plotly_chart(plot_cgpa_by_income_scholarship(df), use_container_width=True)


# --- START: Summary Box and Interpretation ---
st.header("Analysis and Findings", divider="blue")

st.subheader("Summary Box: Socio-economic and Demographic Influence")
with st.container(border=True):
    st.markdown("""
    **Summary (100–150 words):**
    This analysis explores the impact of **gender**, **age/admission year**, and **socio-economic status** on **Current CGPA**. The visualizations show that while average CGPA is similar between genders (as reflected in the metrics), the **Meritorious Scholarship** status is a powerful positive differentiator across all income groups, consistently linking to higher average CGPA. The heatmap reveals a potential academic challenge among older students (25+) across most admission years, as they tend to have slightly lower average CGPAs compared to the younger groups. Overall, financial aid tied to merit appears to be a stronger predictor of academic performance than gender or income group alone.
    """)

st.subheader("Interpretation/Discussion: Observed Patterns")
st.markdown("""
* **Gender Parity:** The box plot and average metrics suggest that there is **no significant academic gap based on gender**. Both male and female CGPA distributions are highly concentrated, indicating similar levels of academic success.
* **Age and Admission Year:** The **Heatmap** shows that the **Age Group (25+)** is associated with lower average CGPAs, particularly for those admitted more recently (2020-2021). This pattern might be due to non-traditional students balancing studies with external commitments (work, family), which can affect time dedicated to coursework.
* **Scholarship as a Predictor:** The grouped bar plot confirms a powerful finding: students receiving a **Meritorious Scholarship** maintain substantially higher CGPAs than their non-scholarship counterparts, *regardless of their family income group*. This suggests that the selection criteria for the scholarship (which is merit-based) effectively identifies students with the highest potential for academic excellence.
""")
# --- END: Summary Box and Interpretation ---

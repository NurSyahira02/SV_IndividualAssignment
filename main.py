import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="Page 1: Household Income Trends",
    layout="wide"
)

st.header("Household Income Growth & Disparity Analysis 📈", divider="gray")

# URL for the dataset
url = "https://github.com/NurSyahira02/SV_IndividualAssignment/blob/main/hh_income_state_CLEANED.csv"

# Load Dataset
try:
    df_income = pd.read_csv('hh_income_state_CLEANED.csv')
    df_income['date'] = pd.to_datetime(df_income['date'])
    df_income['year'] = df_income['date'].dt.year

    # State Selector Dropdown
    selected_state = st.selectbox("Select State / Federal Territory:", sorted(df_income['state'].unique()), index=11)
    
    state_inc = df_income[df_income['state'] == selected_state].sort_values('year')

    # Summary Metrics Calculation
    latest_inc = state_inc[state_inc['year'] == 2024].iloc[0]
    earliest_inc = state_inc[state_inc['year'] == 2019].iloc[0]
    
    mean_growth = ((latest_inc['income_mean'] - earliest_inc['income_mean']) / earliest_inc['income_mean']) * 100
    gap_2024 = latest_inc['income_mean'] - latest_inc['income_median']

    # 4 Summary Boxes
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2024 Mean Income", f"RM {latest_inc['income_mean']:,}", help="Average Household Income in 2024", border=True)
    col2.metric("2024 Median Income", f"RM {latest_inc['income_median']:,}", help="Median Household Income in 2024", border=True)
    col3.metric("5-Year Growth Rate", f"{mean_growth:.1f}%", help="Mean Income Growth from 2019 to 2024", border=True)
    col4.metric("Mean-Median Gap", f"RM {gap_2024:,}", help="Disparity between Mean and Median Income in 2024", border=True)

    # Raw Data Preview
    st.subheader("Raw Data Preview")
    st.dataframe(state_inc[['state', 'year', 'income_mean', 'income_median']])

    # Dual Line Trend Plot
    st.subheader(f"Mean vs. Median Income Trend for {selected_state}")
    
    df_melted = state_inc.melt(
        id_vars=['year'], 
        value_vars=['income_mean', 'income_median'],
        var_name='Metric', 
        value_name='Income (RM)'
    )
    df_melted['Metric'] = df_melted['Metric'].map({'income_mean': 'Mean Income', 'income_median': 'Median Income'})

    fig1 = px.line(
        df_melted,
        x='year',
        y='Income (RM)',
        color='Metric',
        markers=True,
        title=f'Household Income Trajectory in {selected_state} (2019 - 2024)',
        labels={'year': 'Year', 'Income (RM)': 'Income (RM)'},
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    fig1.update_xaxes(type='category')
    fig1.update_layout(hovermode='x unified')

    st.plotly_chart(fig1, use_container_width=True)

    # Interpretation Section
    st.markdown("### 💬 Interpretation & Discussion")
    st.info(f"""
    * **Observed Trend:** In **{selected_state}**, both mean and median household incomes demonstrate an overall upward trajectory from 2019 to 2024.
    * **Income Skewness:** The mean income consistently remains above the median income throughout the period. This positive skew indicates that high-income earners raise the arithmetic average.
    * **Socioeconomic Insight:** The persistent gap between mean and median figures highlights structural income disparity within the region, showing that median income provides a truer representation of typical household welfare.
    """)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")

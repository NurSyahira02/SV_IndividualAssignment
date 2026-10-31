import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="Household Income Analysis",
    layout="wide"
)

st.header("Household Income Growth & Disparity Analysis 📊", divider="gray")

# Load Dataset
try:
    df_income = pd.read_csv('hh_income_state_CLEANED.csv')
    st.success("Data loaded successfully!")
    df_income['date'] = pd.to_datetime(df_income['date'])
    df_income['year'] = df_income['date'].dt.year.astype(str)

    # State Selector Dropdown
    selected_state = st.selectbox("Select State / Federal Territory:", sorted(df_income['state'].unique()), index=11)
    
    state_inc = df_income[df_income['state'] == selected_state].sort_values('year')

    # Summary Metrics Calculation
    latest_inc = state_inc[state_inc['year'] == '2024'].iloc[0]
    earliest_inc = state_inc[state_inc['year'] == '2019'].iloc[0]
    
    mean_growth = ((latest_inc['income_mean'] - earliest_inc['income_mean']) / earliest_inc['income_mean']) * 100
    gap_2024 = latest_inc['income_mean'] - latest_inc['income_median']

   # 4 Summary Boxes
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean Income", f"RM {latest_inc['income_mean']:,}", help="Average household income in 2024 (compared across 2019–2024 baseline)", border=True)
    col2.metric("Median Income", f"RM {latest_inc['income_median']:,}", help="Median household income in 2024 (50th percentile baseline)", border=True)
    col3.metric("5-Year Growth", f"{mean_growth:.1f}%", help="Percentage increase in mean income from 2019 to 2024", border=True)
    col4.metric("Mean-Median Gap", f"RM {gap_2024:,}", help="Difference between mean and median income in 2024 (indicates income disparity)", border=True)

    # Raw Data Preview
    st.subheader("Raw Data Preview")
    st.dataframe(state_inc[['state', 'year', 'income_mean', 'income_median']])

    # Grouped Bar Chart Visualization
    st.subheader(f"Mean vs. Median Income Comparison for {selected_state}")
    
    df_melted = state_inc.melt(
        id_vars=['year'], 
        value_vars=['income_mean', 'income_median'],
        var_name='Metric', 
        value_name='Income (RM)'
    )
    df_melted['Metric'] = df_melted['Metric'].map({'income_mean': 'Mean Income', 'income_median': 'Median Income'})

    fig1 = px.bar(
        df_melted,
        x='year',
        y='Income (RM)',
        color='Metric',
        barmode='group',
        text_auto=',.0f',
        title=f'Household Income Disparity in {selected_state} (2019 - 2024)',
        labels={'year': 'Year', 'Income (RM)': 'Income (RM)'},
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(
        hovermode='x unified',
        height=480,
        legend_title_text='Income Metric'
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Interpretation Section
    st.markdown("### 💬 Interpretation & Discussion")
    st.info(f"""
    * **Observed Growth:** In **{selected_state}**, both mean and median household income bars demonstrate steady expansion between 2019 and 2024.
    * **Distribution Gap:** Side-by-side bar comparisons highlight that mean income consistently exceeds median income across every recorded year.
    * **Socioeconomic Meaning:** The height difference between the mean and median bars visually underscores income inequality, as high-earning households inflate the overall average income.
    """)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")

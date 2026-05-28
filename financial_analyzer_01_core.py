import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📊 Financial Analyzer")
st.subheader("Automated Financial Ratio Analysis Tool")

# File Upload
st.markdown("### 📂 Upload Financial Statements")
col1, col2, col3 = st.columns(3)

with col1:
    income_file = st.file_uploader("Income Statement", type="csv")
with col2:
    balance_file = st.file_uploader("Balance Sheet", type="csv")
with col3:
    cashflow_file = st.file_uploader("Cash Flow Statement", type="csv")

if not (income_file and balance_file and cashflow_file):
    st.warning("Please upload all three CSV files to begin analysis.")
    st.stop()

# Load CSV files
income = pd.read_csv(income_file, index_col='item')
balance = pd.read_csv(balance_file, index_col='item')
cashflow = pd.read_csv(cashflow_file, index_col='item')

years = income.columns.tolist()

st.markdown("---")

# Year selection
selected_year = st.selectbox("Select a year to analyze", years)

st.markdown("---")

# ── Red Flag Helper ──────────────────────────────────────────────
def red_flag(label, value, good_threshold, warning_threshold, higher_is_better=True, unit="x", source=""):
    if higher_is_better:
        if value >= good_threshold:
            status = "🟢"
            reason = f"≥ {good_threshold}{unit} (Good)"
        elif value >= warning_threshold:
            status = "🟡"
            reason = f"Between {warning_threshold}{unit} and {good_threshold}{unit} (Warning)"
        else:
            status = "🔴"
            reason = f"< {warning_threshold}{unit} (Risk)"
    else:
        if value <= good_threshold:
            status = "🟢"
            reason = f"≤ {good_threshold}{unit} (Good)"
        elif value <= warning_threshold:
            status = "🟡"
            reason = f"Between {good_threshold}{unit} and {warning_threshold}{unit} (Warning)"
        else:
            status = "🔴"
            reason = f"> {warning_threshold}{unit} (Risk)"

    st.write(f"{status} **{label}**: {value:.2f}{unit} — {reason} | *Source: {source}*")

# ── Stability ────────────────────────────────────────────────────
st.subheader("🔒 Stability")
with st.expander("ℹ️ How are these calculated?"):
    st.markdown("""
    - **Current Ratio** = Current Assets / Current Liabilities  
      *Airline industry benchmark (Macrotrends, DAL/AAL 2024): 🟢 ≥ 0.5x / 🟡 0.3–0.5x / 🔴 < 0.3x*
    - **Debt Ratio** = Total Liabilities / Total Equity  
      *Airline industry benchmark (IATA Financial Monitor 2024): 🟢 < 3.0x / 🟡 3.0–5.0x / 🔴 > 5.0x*
    - **Interest Coverage Ratio** = Operating Income / Interest Expense  
      *General credit analysis standard: 🟢 ≥ 2.0x / 🟡 1.0–2.0x / 🔴 < 1.0x*
    """)

current_ratio = balance.loc['current_assets', selected_year] / balance.loc['current_liabilities', selected_year]
debt_ratio = balance.loc['total_liabilities', selected_year] / balance.loc['total_equity', selected_year]
interest_coverage = income.loc['operating_income', selected_year] / income.loc['interest_expense', selected_year]

col1, col2, col3 = st.columns(3)
col1.metric("Current Ratio", f"{current_ratio:.2f}x")
col2.metric("Debt Ratio", f"{debt_ratio:.2f}x")
col3.metric("Interest Coverage Ratio", f"{interest_coverage:.2f}x")

st.markdown("**🚦 Red Flag Assessment**")
red_flag("Current Ratio", current_ratio,
         good_threshold=0.5, warning_threshold=0.3,
         higher_is_better=True,
         source="Macrotrends, DAL/AAL 2024")
red_flag("Debt Ratio", debt_ratio,
         good_threshold=3.0, warning_threshold=5.0,
         higher_is_better=False,
         source="IATA Financial Monitor 2024")
red_flag("Interest Coverage Ratio", interest_coverage,
         good_threshold=2.0, warning_threshold=1.0,
         higher_is_better=True,
         source="General credit analysis standard")

st.markdown("---")

# ── Profitability ────────────────────────────────────────────────
st.subheader("💰 Profitability")
with st.expander("ℹ️ How are these calculated?"):
    st.markdown("""
    - **ROA** = Net Income / Total Assets × 100  
      *General standard: 🟢 ≥ 3% / 🟡 1–3% / 🔴 < 1%*
    - **ROE** = Net Income / Total Equity × 100  
      *General standard: 🟢 ≥ 10% / 🟡 5–10% / 🔴 < 5%*
    - **Gross Margin** = Gross Profit / Revenue × 100  
      *General standard: 🟢 ≥ 20% / 🟡 10–20% / 🔴 < 10%*
    - **Operating Margin** = Operating Income / Revenue × 100  
      *Airline industry benchmark (S&P Global Dec 2024): 🟢 ≥ 8% / 🟡 4–8% / 🔴 < 4%*
    - **Net Margin** = Net Income / Revenue × 100  
      *Airline industry benchmark (IATA 2024): 🟢 ≥ 4% / 🟡 0–4% / 🔴 < 0%*
    """)

roa = income.loc['net_income', selected_year] / balance.loc['total_assets', selected_year] * 100
roe = income.loc['net_income', selected_year] / balance.loc['total_equity', selected_year] * 100
gross_margin = income.loc['gross_profit', selected_year] / income.loc['revenue', selected_year] * 100
operating_margin = income.loc['operating_income', selected_year] / income.loc['revenue', selected_year] * 100
net_margin = income.loc['net_income', selected_year] / income.loc['revenue', selected_year] * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("ROA", f"{roa:.2f}%")
col2.metric("ROE", f"{roe:.2f}%")
col3.metric("Gross Margin", f"{gross_margin:.2f}%")
col4.metric("Operating Margin", f"{operating_margin:.2f}%")
col5.metric("Net Margin", f"{net_margin:.2f}%")

st.markdown("**🚦 Red Flag Assessment**")
red_flag("ROA", roa,
         good_threshold=3.0, warning_threshold=1.0,
         higher_is_better=True, unit="%",
         source="General accounting standard")
red_flag("ROE", roe,
         good_threshold=10.0, warning_threshold=5.0,
         higher_is_better=True, unit="%",
         source="General accounting standard")
red_flag("Gross Margin", gross_margin,
         good_threshold=20.0, warning_threshold=10.0,
         higher_is_better=True, unit="%",
         source="General accounting standard")
red_flag("Operating Margin", operating_margin,
         good_threshold=8.0, warning_threshold=4.0,
         higher_is_better=True, unit="%",
         source="S&P Global Dec 2024")
red_flag("Net Margin", net_margin,
         good_threshold=4.0, warning_threshold=0.0,
         higher_is_better=True, unit="%",
         source="IATA 2024")

st.markdown("---")

# ── Efficiency ───────────────────────────────────────────────────
st.subheader("⚙️ Efficiency")
with st.expander("ℹ️ How are these calculated?"):
    st.markdown("""
    - **Asset Turnover** = Revenue / Total Assets  
      *General standard: 🟢 ≥ 0.5x / 🟡 0.3–0.5x / 🔴 < 0.3x*
    - **Inventory Turnover** = Revenue / Inventory  
      *General standard: 🟢 ≥ 10x / 🟡 5–10x / 🔴 < 5x*
    """)

asset_turnover = income.loc['revenue', selected_year] / balance.loc['total_assets', selected_year]
inventory_turnover = income.loc['revenue', selected_year] / balance.loc['inventory', selected_year]

col1, col2 = st.columns(2)
col1.metric("Asset Turnover", f"{asset_turnover:.2f}x")
col2.metric("Inventory Turnover", f"{inventory_turnover:.2f}x")

st.markdown("**🚦 Red Flag Assessment**")
red_flag("Asset Turnover", asset_turnover,
         good_threshold=0.5, warning_threshold=0.3,
         higher_is_better=True,
         source="General accounting standard")
red_flag("Inventory Turnover", inventory_turnover,
         good_threshold=10.0, warning_threshold=5.0,
         higher_is_better=True,
         source="General accounting standard")

st.markdown("---")

# ── Growth ───────────────────────────────────────────────────────
st.subheader("📈 Growth")
with st.expander("ℹ️ How are these calculated?"):
    st.markdown("""
    - **Revenue Growth** = (Current Revenue - Previous Revenue) / Previous Revenue × 100  
      *General standard: 🟢 ≥ 5% / 🟡 0–5% / 🔴 < 0%*
    - **Operating Income Growth** = (Current Operating Income - Previous Operating Income) / Previous Operating Income × 100  
      *General standard: 🟢 ≥ 5% / 🟡 0–5% / 🔴 < 0%*
    """)

year_index = years.index(selected_year)

if year_index == 0:
    st.info("Please select a year after 2020 to calculate growth rates.")
else:
    prev_year = years[year_index - 1]
    revenue_growth = (income.loc['revenue', selected_year] - income.loc['revenue', prev_year]) / income.loc['revenue', prev_year] * 100
    operating_growth = (income.loc['operating_income', selected_year] - income.loc['operating_income', prev_year]) / income.loc['operating_income', prev_year] * 100

    col1, col2 = st.columns(2)
    col1.metric("Revenue Growth", f"{revenue_growth:.2f}%", f"vs {prev_year}")
    col2.metric("Operating Income Growth", f"{operating_growth:.2f}%", f"vs {prev_year}")

    st.markdown("**🚦 Red Flag Assessment**")
    red_flag("Revenue Growth", revenue_growth,
             good_threshold=5.0, warning_threshold=0.0,
             higher_is_better=True, unit="%",
             source="General accounting standard")
    red_flag("Operating Income Growth", operating_growth,
             good_threshold=5.0, warning_threshold=0.0,
             higher_is_better=True, unit="%",
             source="General accounting standard")

st.markdown("---")

# ── Trend Charts ─────────────────────────────────────────────────
st.subheader("📊 Trend Analysis")

chart_data = pd.DataFrame({
    'Year': years,
    'Revenue': [income.loc['revenue', y] for y in years],
    'Gross Profit': [income.loc['gross_profit', y] for y in years],
    'Operating Income': [income.loc['operating_income', y] for y in years],
    'Net Income': [income.loc['net_income', y] for y in years]
})

fig1 = px.line(chart_data, x='Year', y=['Revenue', 'Gross Profit', 'Operating Income', 'Net Income'],
               title='Revenue & Income Trend',
               markers=True)
st.plotly_chart(fig1, use_container_width=True)

margin_data = pd.DataFrame({
    'Year': years,
    'Gross Margin': [income.loc['gross_profit', y] / income.loc['revenue', y] * 100 for y in years],
    'Operating Margin': [income.loc['operating_income', y] / income.loc['revenue', y] * 100 for y in years],
    'Net Margin': [income.loc['net_income', y] / income.loc['revenue', y] * 100 for y in years]
})

fig2 = px.line(margin_data, x='Year', y=['Gross Margin', 'Operating Margin', 'Net Margin'],
               title='Profitability Margin Trend (%)',
               markers=True)
st.plotly_chart(fig2, use_container_width=True)

return_data = pd.DataFrame({
    'Year': years,
    'ROA': [income.loc['net_income', y] / balance.loc['total_assets', y] * 100 for y in years],
    'ROE': [income.loc['net_income', y] / balance.loc['total_equity', y] * 100 for y in years]
})

fig3 = px.line(return_data, x='Year', y=['ROA', 'ROE'],
               title='Return Ratios Trend (%)',
               markers=True)
st.plotly_chart(fig3, use_container_width=True)

stability_data = pd.DataFrame({
    'Year': years,
    'Current Ratio': [balance.loc['current_assets', y] / balance.loc['current_liabilities', y] for y in years],
    'Debt Ratio': [balance.loc['total_liabilities', y] / balance.loc['total_equity', y] for y in years],
    'Interest Coverage': [income.loc['operating_income', y] / income.loc['interest_expense', y] for y in years]
})

fig4 = px.line(stability_data, x='Year', y=['Current Ratio', 'Debt Ratio', 'Interest Coverage'],
               title='Stability Ratios Trend',
               markers=True)
st.plotly_chart(fig4, use_container_width=True)
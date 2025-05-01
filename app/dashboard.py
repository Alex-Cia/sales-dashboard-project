import streamlit as st
import pandas as pd
import altair as alt
import os

# --- Load Data ---
DATA_PATH = os.path.join('data', 'CloudNova_Sales_Data_2015_2024.csv')
df = pd.read_csv(DATA_PATH)

# --- Page Setup ---
st.set_page_config(page_title="CloudNova Sales Dashboard", layout="wide")

st.title("📊 CloudNova Sales Dashboard")
st.markdown("Welcome to the interactive sales dashboard for **CloudNova Retail Ltd.**")

# --- Sidebar Filters ---
st.sidebar.header("📂 Filter Sales Data")

# --- Year Filter with Select All ---
all_years = sorted(df['year'].unique())
select_all_years = st.sidebar.checkbox("Select All Years", value=True)
if select_all_years:
    years = st.sidebar.multiselect("Select Year(s)", all_years, default=all_years)
else:
    years = st.sidebar.multiselect("Select Year(s)", all_years)

# --- Region Filter with Select All ---
all_regions = sorted(df['region'].unique())
select_all_regions = st.sidebar.checkbox("Select All Regions", value=True)
if select_all_regions:
    regions = st.sidebar.multiselect("Select Region(s)", all_regions, default=all_regions)
else:
    regions = st.sidebar.multiselect("Select Region(s)", all_regions)

# --- Product Category Filter with Select All ---
all_categories = sorted(df['product_category'].unique())
select_all_categories = st.sidebar.checkbox("Select All Categories", value=True)
if select_all_categories:
    categories = st.sidebar.multiselect("Select Product Category(ies)", all_categories, default=all_categories)
else:
    categories = st.sidebar.multiselect("Select Product Category(ies)", all_categories)

# --- Filtered Data ---
filtered_df = df[
    (df['year'].isin(years)) &
    (df['region'].isin(regions)) &
    (df['product_category'].isin(categories))
].copy()

# --- Summary KPIs ---
total_sales = filtered_df['sales'].sum()
total_profit = filtered_df['profit'].sum()
avg_monthly_sales = filtered_df['sales'].mean()
avg_monthly_profit = filtered_df['profit'].mean()

st.subheader("🔢 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Monthly Sales", f"${avg_monthly_sales:,.2f}")
col4.metric("Avg Monthly Profit", f"${avg_monthly_profit:,.2f}")

# --- Profit by Product Category Chart ---
st.subheader("📦 Profit by Product Category")
category_profit = (
    filtered_df.groupby('product_category')['profit']
    .sum()
    .reset_index()
    .sort_values(by='profit', ascending=False)
)
category_chart = alt.Chart(category_profit).mark_bar(color='#BB38DE').encode(
    x=alt.X('product_category:N', title='Product Category'),
    y=alt.Y('profit:Q', title='Total Profit'),
    tooltip=['product_category', 'profit']
).properties(width=600, height=400)
st.altair_chart(category_chart, use_container_width=True)

# --- Profit by Region Chart ---
st.subheader("🌍 Profit by Region")
region_profit = (
    filtered_df.groupby('region')['profit']
    .sum()
    .reset_index()
    .sort_values(by='profit', ascending=False)
)
region_chart = alt.Chart(region_profit).mark_bar(color='#00A88E').encode(
    x=alt.X('region:N', title='Region'),
    y=alt.Y('profit:Q', title='Total Profit'),
    tooltip=['region', 'profit']
).properties(width=600, height=400)
st.altair_chart(region_chart, use_container_width=True)

# --- Profit by Month (Seasonal Trend) ---
st.subheader("📆 Profit by Month (Seasonal Trend)")
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
monthly_profit = (
    filtered_df.groupby('month')['profit']
    .sum()
    .reindex(month_order)
    .reset_index()
)
monthly_chart = alt.Chart(monthly_profit).mark_bar(color='#EF6A00').encode(
    x=alt.X('month:N', sort=month_order, title='Month'),
    y=alt.Y('profit:Q', title='Total Profit'),
    tooltip=['month', 'profit']
).properties(width=800, height=400)
st.altair_chart(monthly_chart, use_container_width=True)

# --- Profit by Sales Channel ---
st.subheader("🛍️ Profit by Sales Channel")
channel_profit = (
    filtered_df.groupby('channel')['profit']
    .sum()
    .reset_index()
    .sort_values(by='profit', ascending=False)
)
channel_chart = alt.Chart(channel_profit).mark_bar(color='#AE905F').encode(
    x=alt.X('channel:N', title='Sales Channel'),
    y=alt.Y('profit:Q', title='Total Profit'),
    tooltip=['channel', 'profit']
).properties(width=600, height=400)
st.altair_chart(channel_chart, use_container_width=True)

# --- Profit Trend Over Time (Line Chart) ---
st.subheader("📈 Profit Trend Over Time")
month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
             'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
filtered_df['month_num'] = filtered_df['month'].map(month_map)
filtered_df['date'] = pd.to_datetime(filtered_df['year'].astype(str) + '-' + filtered_df['month_num'].astype(str))
profit_over_time = (
    filtered_df.groupby('date')['profit']
    .sum()
    .reset_index()
    .sort_values('date')
)
trend_chart = alt.Chart(profit_over_time).mark_line(color='#00539F', point=True).encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y('profit:Q', title='Profit'),
    tooltip=['date', 'profit']
).properties(width=800, height=400)
st.altair_chart(trend_chart, use_container_width=True)
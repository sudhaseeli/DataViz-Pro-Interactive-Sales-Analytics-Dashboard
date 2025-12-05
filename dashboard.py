import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataViz Pro Dashboard", layout="wide")

st.title("📊 DataViz Pro — Interactive Sales Dashboard")
st.caption("Analyze sales trends, categories, regions, and KPIs in real time")

# Upload or sample
uploaded = st.file_uploader("Upload Sales CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/sample_sales.csv")
    st.info("Using sample dataset (sample_sales.csv)")

# Convert date
df['date'] = pd.to_datetime(df['date'])

# KPI Row
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Revenue", f"${df['amount'].sum():,.0f}")
kpi2.metric("Total Orders", len(df))
kpi3.metric("Avg Order Value", f"${df['amount'].mean():.2f}")

# Filters
regions = st.multiselect("Filter by Region", df['region'].unique(), default=df['region'].unique())
categories = st.multiselect("Filter by Category", df['category'].unique(), default=df['category'].unique())

filtered = df[df['region'].isin(regions) & df['category'].isin(categories)]

# Charts
st.subheader("📈 Sales Trend Over Time")
fig_trend = px.line(filtered, x="date", y="amount", title="Daily Sales Trend", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("📊 Revenue by Category")
fig_cat = px.bar(filtered.groupby('category')['amount'].sum().reset_index(),
                 x='category', y='amount', color='category',
                 title="Category Performance", text='amount')
st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("🌍 Revenue by Region")
fig_region = px.pie(filtered, names='region', values='amount', title="Region Share")
st.plotly_chart(fig_region, use_container_width=True)

# Heatmap
st.subheader("🔥 Category vs Region Heatmap")
heat = filtered.pivot_table(index='category', columns='region', values='amount', aggfunc='sum')
fig_heat = px.imshow(heat, text_auto=True, title="Heatmap: Category × Region Revenue")
st.plotly_chart(fig_heat, use_container_width=True)

# Forecast Preview (SMA)
st.subheader("🔮 Forecast Preview (Simple Moving Average)")
tmp = filtered.groupby('date')['amount'].sum().rolling(3).mean()
fig_forecast = px.line(tmp, title="3-Day Moving Average Forecast", markers=True)
st.plotly_chart(fig_forecast, use_container_width=True)

st.success("Dashboard Loaded Successfully 🎉")
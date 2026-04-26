# import streamlit as st
# import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")

import streamlit as st
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
# Path adjusted to your local setup
df = pd.read_csv(output_path)

# Ensure date format using your column: InvoiceDate
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Dashboard")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

# 📅 Date filter
min_date = df['InvoiceDate'].min()
max_date = df['InvoiceDate'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# 🌍 Country filter (replaces Region)
countries = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

# 🏷️ Product filter (using Description as Category)
products = st.sidebar.multiselect(
    "Select Product Description",
    options=df['Description'].unique()[:20], # Limited to top 20 for performance
    default=None 
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df.copy()

# Apply date filter
if isinstance(date_range, list) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['InvoiceDate'] >= pd.to_datetime(start_date)) &
        (filtered_df['InvoiceDate'] <= pd.to_datetime(end_date))
    ]

# Apply country filter
filtered_df = filtered_df[filtered_df['Country'].isin(countries)]

# Apply product description filter (if selected)
if products:
    filtered_df = filtered_df[filtered_df['Description'].isin(products)]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

# Using your 'Sales' and 'InvoiceNo' columns
total_revenue = filtered_df['Sales'].sum()
total_orders = filtered_df['InvoiceNo'].nunique() # Count unique invoices
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Invoices", total_orders)
col3.metric("Avg Invoice Value", f"${avg_order_value:,.2f}")


# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📊 Insights")

col1, col2 = st.columns(2)

# Sales by Country
with col1:
    st.write("### Sales by Country")
    country_sales = filtered_df.groupby('Country')['Sales'].sum().sort_values(ascending=False)
    st.bar_chart(country_sales)

# Quantity by Country
with col2:
    st.write("### Units Sold by Country")
    country_qty = filtered_df.groupbys('Country')['Quantity'].sum().sort_values(ascending=False)
    st.bar_chart(country_qty,y="Quantity")

# -----------------------------
# MONTHLY TREND
# -----------------------------
st.write("### 📈 Monthly Sales Trend")

# Grouping by the InvoiceDate
monthly_sales = (
    filtered_df
    .groupby(filtered_df['InvoiceDate'].dt.to_period("M"))['Sales']
    .sum()
    .reset_index()
)

monthly_sales['InvoiceDate'] = monthly_sales['InvoiceDate'].astype(str)

st.line_chart(monthly_sales.set_index('InvoiceDate'),y="Sales")

# -----------------------------
# TOP PRODUCTS
# -----------------------------
st.write("### 🏆 Top 10 Products by Sales")

top_products = (
    filtered_df
    .groupby('Description')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.table(top_products)
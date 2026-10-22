import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("Interactive Sales Dashboard")
st.write("Analyze sales by year, region, and product.")

# Generate sample sales data
np.random.seed(42)

df = pd.DataFrame({
    "Year": np.random.choice([2022, 2023, 2024], 200),
    "Region": np.random.choice(
        ["North", "South", "East", "West"], 200
    ),
    "Product": np.random.choice(["A", "B", "C"], 200),
    "Sales": np.random.randint(1000, 10000, 200)
})

# Sidebar filters
st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

product = st.sidebar.multiselect(
    "Product",
    sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

# Filter the data
filtered = df[
    (df["Year"].isin(year)) &
    (df["Region"].isin(region)) &
    (df["Product"].isin(product))
]

# Display KPIs
st.subheader("Key Performance Indicators")

c1, c2, c3 = st.columns(3)

total_sales = filtered["Sales"].sum()
average_sales = filtered["Sales"].mean()
records = len(filtered)

c1.metric("Total Sales", f"{total_sales:,}")
c2.metric(
    "Average Sales",
    f"{average_sales:,.2f}" if records else "0"
)
c3.metric("Records", records)

st.divider()

# Display charts
st.subheader("Sales by Region")

region_sales = filtered.groupby("Region")["Sales"].sum()
st.bar_chart(region_sales)

st.subheader("Sales by Year")

year_sales = filtered.groupby("Year")["Sales"].sum()
st.line_chart(year_sales)



# Exercise 1: Pie chart
st.subheader("Sales by Product")

product_sales = filtered.groupby("Product")["Sales"].sum()

if not product_sales.empty:
    fig = px.pie(
        names=product_sales.index,
        values=product_sales.values,
        title="Sales Distribution by Product"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No sales data for the selected filters.")

# Exercise 2: Download filtered data
st.subheader("Download Filtered Data")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

st.caption("Dashboard data is randomly generated for practice.")

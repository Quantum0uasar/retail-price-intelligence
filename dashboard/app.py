import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(
    page_title="Retail Price Intelligence",
    layout="wide"
)

st.title("Retail Price Elasticity & Demand Intelligence Dashboard")
st.caption("Strategic Pricing Recommendations for a Retail Client")


# -----------------------------
# LOAD DATA
# -----------------------------

elasticity = pd.read_csv(
    "data/processed/elasticity_results.csv"
)

customers = pd.read_csv(
    "data/processed/customer_segments.csv"
)


# -----------------------------
# PRICE ELASTICITY SECTION
# -----------------------------

st.header("1. Price Sensitivity by Category")

valid_categories = elasticity[
    elasticity["elasticity"] < 0
].copy()

category = st.selectbox(
    "Choose a product category",
    valid_categories["category"].sort_values()
)

row = valid_categories[
    valid_categories["category"] == category
].iloc[0]

elasticity_value = row["elasticity"]

st.metric(
    "Estimated Price Elasticity",
    f"{elasticity_value:.2f}"
)

st.write(
    "More negative values mean customer demand tends to react more strongly to price changes."
)


# -----------------------------
# PRICE SIMULATION
# -----------------------------

st.header("2. Price Change Simulator")

price_change = st.slider(
    "Simulated price change (%)",
    min_value=-20,
    max_value=20,
    value=0
)

estimated_demand_change = (
    elasticity_value * price_change
)

estimated_revenue_change = (
    (1 + price_change / 100)
    * (1 + estimated_demand_change / 100)
    - 1
) * 100

col1, col2 = st.columns(2)

col1.metric(
    "Estimated Demand Change",
    f"{estimated_demand_change:.1f}%"
)

col2.metric(
    "Estimated Revenue Change",
    f"{estimated_revenue_change:.1f}%"
)


# -----------------------------
# ELASTICITY CHART
# -----------------------------

chart_data = (
    valid_categories
    .sort_values("elasticity")
    .head(15)
)

fig = px.bar(
    chart_data,
    x="elasticity",
    y="category",
    orientation="h",
    title="Most Price-Sensitive Categories"
)

st.plotly_chart(
    fig,
    width='stretch'
)


# -----------------------------
# CUSTOMER SEGMENTS
# -----------------------------

st.header("3. Customer Segmentation")

segment_summary = (
    customers.groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_spend=("monetary", "mean")
    )
    .reset_index()
)

fig2 = px.bar(
    segment_summary,
    x="segment",
    y="customers",
    title="Customers by Segment",
    text="customers"
)

st.plotly_chart(
    fig2,
    width='stretch'
)

st.dataframe(
    segment_summary.round(2),
    width='stretch'
)


# -----------------------------
# CONSULTING TAKEAWAY
# -----------------------------

st.header("4. Strategic Recommendation")

if elasticity_value < -1:
    st.warning(
        "This category appears price-sensitive. Large price increases may reduce demand enough to hurt revenue."
    )
else:
    st.success(
        "This category appears relatively less price-sensitive. Moderate price increases may have lower demand risk."
    )

st.caption(
    "Elasticity estimates are based on historical observational data and should be treated as directional signals, not causal forecasts."
)

# -----------------------------
# CATEGORY COMMERCIAL PERFORMANCE
# -----------------------------

import sqlite3

st.header("5. Category Commercial Performance")

con = sqlite3.connect("database/retail.db")

category_query = """
SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name
    ) AS category,
    COUNT(*) AS units_sold,
    AVG(oi.price) AS avg_price,
    SUM(oi.price) AS revenue,
    AVG(oi.freight_value / oi.price) * 100 AS freight_burden
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE oi.price > 0
GROUP BY category
"""

performance = pd.read_sql_query(category_query, con)
con.close()

performance = performance.sort_values(
    "revenue",
    ascending=False
).head(20)

fig3 = px.scatter(
    performance,
    x="avg_price",
    y="revenue",
    size="units_sold",
    color="freight_burden",
    hover_name="category",
    title="Category Revenue, Pricing and Freight Burden"
)

st.plotly_chart(fig3, width='stretch')

st.caption(
    "Bubble size represents units sold. Colour represents shipping cost relative to product price."
)

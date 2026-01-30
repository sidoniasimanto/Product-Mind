import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# =========================================
# CONFIG
# =========================================

API_BASE_URL = "https://product-mind-2.onrender.com"

st.set_page_config(
    page_title="Product Performance Dashboard",
    layout="wide"
)

st.title("📊 Product Performance Dashboard")

st.caption("Note: Backend may take 30–60 seconds to wake up (free hosting).")

# =========================================
# SAFE FETCH FUNCTION (COLD START PROTECTED)
# =========================================

def fetch(endpoint, retries=8, delay=3):
    url = f"{API_BASE_URL}{endpoint}"
    placeholder = st.empty()

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                placeholder.empty()
                return response.json()

            placeholder.warning(
                f"Backend waking up... Attempt {attempt+1}/{retries}"
            )

        except requests.exceptions.RequestException:
            placeholder.warning(
                f"Connecting to backend... Attempt {attempt+1}/{retries}"
            )

        time.sleep(delay)

    placeholder.error("Backend unavailable. Please refresh.")
    return None

# =========================================
# FETCH DATA
# =========================================

metrics = fetch("/metrics/products")
decisions = fetch("/products/decisions")

if not metrics or not decisions:
    st.stop()

df_metrics = pd.DataFrame(metrics)
df_decisions = pd.DataFrame(decisions)

df = df_metrics.merge(
    df_decisions[["product_id", "recommended_action", "forecast_risk"]],
    on="product_id",
    how="left"
)

# =========================================
# KPIs
# =========================================

total_revenue = df["total_revenue"].sum()
avg_margin = df["profit_margin"].mean()

top_category = (
    df.groupby("category")["total_revenue"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Average Profit Margin", f"{avg_margin:.1%}")
col3.metric("Top Selling Category", top_category)

# =========================================
# CATEGORY HEATMAP
# =========================================

st.subheader("Category Performance Heatmap")

heatmap_data = (
    df.groupby("category")
    .agg({
        "total_revenue": "sum",
        "profit_margin": "mean"
    })
    .reset_index()
)

fig = px.density_heatmap(
    heatmap_data,
    x="category",
    y="profit_margin",
    z="total_revenue",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# TABLE
# =========================================

st.subheader("Product Performance Table")

st.dataframe(
    df[[
        "product_id",
        "product_name",
        "category",
        "total_units_sold",
        "total_revenue",
        "profit_margin",
        "recommended_action",
        "forecast_risk"
    ]],
    use_container_width=True
)

# =========================================
# SIMPLE RULE-BASED ASSISTANT
# =========================================

st.subheader("💬 Executive Assistant")

question = st.text_input("Ask about portfolio risk, growth, or summary:")

if question:
    q = question.lower()

    high = df[df["forecast_risk"] == "HIGH_RISK"]
    medium = df[df["forecast_risk"] == "MEDIUM_RISK"]
    stable = df[df["forecast_risk"] == "STABLE"]
    growth = df[df["recommended_action"] == "SCALE_UP"]

    if "high risk" in q:
        st.write(high[["product_name", "forecast_risk"]])

    elif "medium risk" in q:
        st.write(medium[["product_name", "forecast_risk"]])

    elif "stable" in q:
        st.write(stable[["product_name", "forecast_risk"]])

    elif "growth" in q or "scale" in q:
        st.write(growth[["product_name", "recommended_action"]])

    elif "summary" in q:
        st.write(
            f"""
            Portfolio Summary:
            - High Risk: {len(high)}
            - Medium Risk: {len(medium)}
            - Stable: {len(stable)}
            - Growth: {len(growth)}
            """
        )

    else:
        st.write("Please ask about high risk, medium risk, growth or summary.")

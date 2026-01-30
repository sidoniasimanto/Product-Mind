import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "https://product-mind-2.onrender.com"

st.set_page_config(page_title="ProductMind AI", layout="wide")

st.title("📊 Product Performance Dashboard")

def fetch(endpoint):
    return requests.get(f"{API_BASE_URL}{endpoint}").json()

# ---------------- FETCH DATA ----------------

metrics = fetch("/metrics/products")
decisions = fetch("/products/decisions")

df_metrics = pd.DataFrame(metrics)
df_decisions = pd.DataFrame(decisions)

# Safe merge (avoid duplicate column conflicts)
df = df_metrics.merge(
    df_decisions[[
        "product_id",
        "recommended_action",
        "risk_level"
    ]],
    on="product_id",
    how="left"
)

# ---------------- KPI ROW ----------------

total_revenue = df["total_revenue"].sum()
avg_margin = df["profit_margin"].mean()

top_category = (
    df.groupby("category")["total_revenue"]
    .sum()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Average Profit Margin", f"{avg_margin:.1%}")
col3.metric("Top Selling Category", top_category)

st.divider()

# ---------------- HEATMAP ----------------

st.subheader("Category Risk Distribution")

heatmap_data = (
    df.groupby(["category", "risk_level"])["total_revenue"]
    .sum()
    .reset_index()
)

fig = px.density_heatmap(
    heatmap_data,
    x="category",
    y="risk_level",
    z="total_revenue",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- PRODUCT TABLE ----------------

st.subheader("Product Overview")

display_df = df[[
    "product_id",
    "product_name",
    "category",
    "total_units_sold",
    "total_revenue",
    "profit_margin",
    "risk_level",
    "recommended_action"
]]

st.dataframe(display_df, use_container_width=True)

# =====================================================
# SIMPLE RULE-BASED ASSISTANT
# =====================================================

st.divider()
st.subheader("💬 Executive Assistant")

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if st.button("Open Assistant"):
    st.session_state.chat_open = True

if st.session_state.chat_open:

    user_input = st.text_input("Ask a portfolio question:")

    if user_input:

        question = user_input.lower()

        high_risk = df[df["risk_level"] == "HIGH_RISK"]
        medium_risk = df[df["risk_level"] == "MEDIUM_RISK"]
        low_risk = df[df["risk_level"] == "LOW_RISK"]
        stable = df[df["risk_level"] == "STABLE"]

        if "high risk" in question:
            st.write("### High Risk Products")
            st.dataframe(high_risk[[
                "product_name",
                "category",
                "profit_margin",
                "total_revenue"
            ]])

        elif "medium risk" in question:
            st.write("### Medium Risk Products")
            st.dataframe(medium_risk[[
                "product_name",
                "category",
                "profit_margin",
                "total_revenue"
            ]])

        elif "low risk" in question:
            st.write("### Low Risk Products")
            st.dataframe(low_risk[[
                "product_name",
                "category",
                "profit_margin",
                "total_revenue"
            ]])

        elif "stable" in question:
            st.write("### Stable Products")
            st.dataframe(stable[[
                "product_name",
                "category",
                "profit_margin",
                "total_revenue"
            ]])

        elif "summary" in question or "overview" in question:

            st.markdown(f"""
            **Portfolio Summary**

            • High Risk: {len(high_risk)}  
            • Medium Risk: {len(medium_risk)}  
            • Low Risk: {len(low_risk)}  
            • Stable: {len(stable)}

            Total Revenue: ${total_revenue:,.0f}
            """)

        else:
            st.write("Please ask about: high risk, medium risk, low risk, stable, or summary.")

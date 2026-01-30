import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time

API_BASE_URL = "https://product-mind-2.onrender.com"

st.set_page_config(
    page_title="Decision Engine",
    layout="wide"
)

st.title("⚙️ Product Decision Engine")

# =========================================
# SAFE FETCH
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

        except:
            placeholder.warning(
                f"Connecting to backend... Attempt {attempt+1}/{retries}"
            )

        time.sleep(delay)

    placeholder.error("Backend unavailable. Please refresh.")
    return None

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
# PRODUCT SELECTOR
# =========================================

product_map = {
    f"{row['product_name']} ({row['product_id']})": row["product_id"]
    for _, row in df.iterrows()
}

selected_label = st.selectbox("Select Product", list(product_map.keys()))
selected_id = product_map[selected_label]

row = df[df["product_id"] == selected_id].iloc[0]

revenue = row["total_revenue"]
margin = row["profit_margin"]

col1, col2 = st.columns(2)
col1.metric("Revenue", f"${revenue:,.0f}")
col2.metric("Profit Margin", f"{margin:.1%}")

# =========================================
# SCENARIO SIMULATION
# =========================================

st.subheader("Scenario Simulation")

price = st.slider("Increase Price %", -20, 20, 0)
marketing = st.slider("Increase Marketing %", 0, 50, 0)
cost = st.slider("Reduce Cost %", 0, 30, 0)

sim_revenue = revenue * (1 + price/100) * (1 + marketing/100)
sim_margin = margin + cost/100 - price/200

st.metric("Projected Revenue", f"${sim_revenue:,.0f}")
st.metric("Projected Margin", f"{sim_margin:.1%}")

# =========================================
# FORECAST GRAPH
# =========================================

if st.button("Show Forecast"):

    history = [revenue*0.7, revenue*0.8, revenue*0.9, revenue]
    forecast = [sim_revenue*1.05, sim_revenue*1.1]

    series = history + forecast
    periods = list(range(len(series)))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=periods,
        y=series,
        mode="lines+markers"
    ))

    fig.update_layout(
        template="plotly_white",
        title="Revenue Forecast"
    )

    st.plotly_chart(fig, use_container_width=True)

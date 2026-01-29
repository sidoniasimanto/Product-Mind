import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_BASE_URL = "https://product-mind-2.onrender.com"

st.set_page_config(page_title="Decision Engine", layout="wide")

def fetch(endpoint):
    return requests.get(f"{API_BASE_URL}{endpoint}").json()


metrics = fetch("/metrics/products")
df = pd.DataFrame(metrics)

st.title("⚙️ Product Decision Engine")

selected = st.selectbox(
    "Select Product",
    df["product_name"]
)

row = df[df["product_name"] == selected].iloc[0]

col1, col2 = st.columns(2)

col1.metric("Revenue", f"${row['total_revenue']:,.0f}")
col2.metric("Margin", f"{row['profit_margin']:.1%}")

st.divider()

# ---------- SCENARIO SIMULATION ----------

st.subheader("Scenario Simulation")

price = st.slider("Increase Price %", -20, 20, 0)
marketing = st.slider("Increase Marketing %", 0, 50, 0)
cost = st.slider("Reduce Cost %", 0, 30, 0)

sim_revenue = row["total_revenue"] * (1 + price/100) * (1 + marketing/100)
sim_margin = row["profit_margin"] + cost/100 - price/200

col3, col4 = st.columns(2)
col3.metric("Projected Revenue", f"${sim_revenue:,.0f}")
col4.metric("Projected Margin", f"{sim_margin:.1%}")

st.divider()

# ---------- FORECAST ----------

if st.button("Show Forecast"):

    history = [
        row["total_revenue"] * 0.7,
        row["total_revenue"] * 0.85,
        row["total_revenue"]
    ]

    forecast = [
        sim_revenue * 1.05,
        sim_revenue * 1.1
    ]

    series = history + forecast

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(series))),
        y=series,
        mode="lines+markers"
    ))

    fig.update_layout(
        template="simple_white",
        title="Revenue Forecast"
    )

    st.plotly_chart(fig, use_container_width=True)

from fastapi import FastAPI
from backend.analytics.product_metrics import calculate_product_metrics
from backend.agents.product_agent import ProductAgent

app = FastAPI()
agent = ProductAgent()


@app.get("/metrics/products")
def get_product_metrics():
    df = calculate_product_metrics()
    return df.to_dict(orient="records")


@app.get("/products/decisions")
def get_product_decisions():
    decisions = agent.run()
    return decisions


@app.get("/products/decisions/explain")
def explain_decisions():
    decisions = agent.run()
    return [agent.explain(d) for d in decisions]

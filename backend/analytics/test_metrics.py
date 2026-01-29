from backend.analytics.product_metrics import calculate_product_metrics

metrics = calculate_product_metrics()

print(metrics.sort_values("total_profit", ascending=False).head())

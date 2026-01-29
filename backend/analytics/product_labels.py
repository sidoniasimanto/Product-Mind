from backend.analytics.product_metrics import calculate_product_metrics
from backend.analytics.trend_analysis import detect_declining_products


def label_products():
    metrics = calculate_product_metrics()
    trends = detect_declining_products()

    trend_map = {t["product_id"]: t["trend"] for t in trends}

    labels = []

    for _, row in metrics.iterrows():
        product_id = row["product_id"]
        margin = row["profit_margin"]
        trend = trend_map.get(product_id, 0)

        if margin > 0.4 and trend > 0:
            status = "PROMOTE"
        elif margin < 0.2 and trend < 0:
            status = "DISCONTINUE"
        elif trend < 0:
            status = "MONITOR"
        else:
            status = "STABLE"

        labels.append({
            "product_id": product_id,
            "status": status,
            "profit_margin": round(margin, 2),
            "trend": trend
        })

    return labels

import pandas as pd
from backend.analytics.business_view import create_product_sales_view


def detect_declining_products():
    """
    Detects products with declining sales trends.
    """

    df = create_product_sales_view()

    # Correct datetime conversion
    df["date"] = pd.to_datetime(df["date"])

    trends = []

    for product_id, group in df.groupby("product_id"):
        group = group.sort_values("date")

        if len(group) < 2:
            continue

        recent = group.tail(1)["units_sold"].values[0]
        previous = group.tail(2).head(1)["units_sold"].values[0]

        trend = recent - previous

        trends.append({
            "product_id": product_id,
            "trend": trend
        })

    return trends

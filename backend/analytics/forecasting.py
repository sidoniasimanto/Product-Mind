import pandas as pd
from backend.analytics.business_view import create_product_sales_view


def forecast_product_demand(months_ahead=3):
    """
    Forecasts future product demand using recent trends.
    """

    df = create_product_sales_view()
    df["date"] = pd.to_datetime(df["date"])

    forecasts = []

    for product_id, group in df.groupby("product_id"):
        group = group.sort_values("date")

        if len(group) < 3:
            continue

        # Simple trend: average change in last 3 periods
        recent = group.tail(3)
        deltas = recent["units_sold"].diff().dropna()

        avg_trend = deltas.mean()

        last_units = recent.iloc[-1]["units_sold"]
        forecast_units = max(
            int(last_units + avg_trend * months_ahead),
            0
        )

        forecasts.append({
            "product_id": product_id,
            "last_units_sold": int(last_units),
            "avg_trend_per_period": round(avg_trend, 2),
            "forecast_units_next_period": forecast_units
        })

    return forecasts

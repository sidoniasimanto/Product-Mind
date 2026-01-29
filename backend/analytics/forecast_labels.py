from backend.analytics.forecasting import forecast_product_demand


def label_forecast_risk():
    forecasts = forecast_product_demand()

    labeled = []

    for f in forecasts:
        change = f["forecast_units_next_period"] - f["last_units_sold"]

        if change < -20:
            risk = "HIGH_RISK"
        elif change < 0:
            risk = "MEDIUM_RISK"
        elif change > 20:
            risk = "HIGH_OPPORTUNITY"
        else:
            risk = "STABLE"

        labeled.append({
            "product_id": f["product_id"],
            "forecast_change": change,
            "forecast_risk": risk
        })

    return labeled

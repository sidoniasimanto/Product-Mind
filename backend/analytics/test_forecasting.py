from backend.analytics.forecasting import forecast_product_demand

forecasts = forecast_product_demand(months_ahead=3)

for f in forecasts[:10]:
    print(f)

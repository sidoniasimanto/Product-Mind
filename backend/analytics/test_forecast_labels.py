from backend.analytics.forecast_labels import label_forecast_risk

labels = label_forecast_risk()

for l in labels[:10]:
    print(l)

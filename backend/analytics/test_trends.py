from backend.analytics.trend_analysis import detect_declining_products

trends = detect_declining_products()

declining = [t for t in trends if t["trend"] < 0]

print("Declining products:")
print(declining)

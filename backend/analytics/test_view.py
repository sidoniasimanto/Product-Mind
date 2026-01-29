from backend.analytics.business_view import create_product_sales_view

df = create_product_sales_view()

print(df.head())
print("\nColumns:")
print(df.columns)

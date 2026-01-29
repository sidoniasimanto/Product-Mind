from backend.core.data_loader import load_products

products = load_products()
print(products.head())

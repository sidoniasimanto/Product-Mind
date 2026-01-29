from backend.analytics.product_labels import label_products

labels = label_products()

for l in labels[:10]:
    print(l)

def validate_products(df):
    required_columns = [
        "product_id", "name", "category",
        "cost_price", "selling_price"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    if not (df["selling_price"] > df["cost_price"]).all():
        raise ValueError("Selling price must be greater than cost price")

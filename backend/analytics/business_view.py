from backend.core.data_loader import load_products, load_sales


def create_product_sales_view():
    """
    Creates a combined dataset of product + sales data
    and calculates revenue and profit.
    """

    # Load raw data
    products = load_products()
    sales = load_sales()

    # Combine sales with product details
    merged = sales.merge(products, on="product_id")

    # Business calculations
    merged["revenue"] = merged["units_sold"] * merged["selling_price"]
    merged["profit"] = merged["units_sold"] * (
        merged["selling_price"] - merged["cost_price"]
    )

    return merged

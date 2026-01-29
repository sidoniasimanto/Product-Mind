from backend.analytics.business_view import create_product_sales_view


def calculate_product_metrics():
    """
    Calculates revenue, profit, margin and units sold per product.
    """

    df = create_product_sales_view()

    grouped = df.groupby(
        ["product_id", "name", "category"]
    ).agg(
        total_units_sold=("units_sold", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum")
    ).reset_index()

    # Rename to match frontend expectations
    grouped = grouped.rename(columns={"name": "product_name"})

    # Safe margin calculation
    grouped["profit_margin"] = (
        grouped["total_profit"] / grouped["total_revenue"]
    )

    return grouped

import pandas as pd
from .config import RAW_DATA_DIR


def load_products():
    return pd.read_csv(RAW_DATA_DIR / "products.csv")


def load_customers():
    return pd.read_csv(RAW_DATA_DIR / "customers.csv")


def load_orders():
    return pd.read_csv(RAW_DATA_DIR / "orders.csv")


def load_sales():
    return pd.read_csv(RAW_DATA_DIR / "sales_daily.csv")


def load_inventory():
    return pd.read_csv(RAW_DATA_DIR / "inventory.csv")

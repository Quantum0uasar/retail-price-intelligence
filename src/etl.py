import sqlite3
import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
DB = Path("database/retail.db")

DB.parent.mkdir(exist_ok=True)


# -----------------------------
# LOAD CSV FILES
# -----------------------------

customers = pd.read_csv(RAW / "olist_customers_dataset.csv")
orders = pd.read_csv(RAW / "olist_orders_dataset.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
products = pd.read_csv(RAW / "olist_products_dataset.csv")
payments = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
categories = pd.read_csv(RAW / "product_category_name_translation.csv")


# -----------------------------
# CLEAN ORDERS
# -----------------------------

# Keep completed sales only
orders = orders[orders["order_status"] == "delivered"].copy()

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# -----------------------------
# CLEAN ORDER ITEMS
# -----------------------------

items["shipping_limit_date"] = pd.to_datetime(
    items["shipping_limit_date"],
    errors="coerce"
)

items = items[
    (items["price"] > 0) &
    (items["freight_value"] >= 0)
].copy()


# -----------------------------
# CLEAN PRODUCTS
# -----------------------------

products["product_category_name"] = (
    products["product_category_name"]
    .fillna("unknown")
)


# -----------------------------
# REMOVE DUPLICATES
# -----------------------------

customers = customers.drop_duplicates()
orders = orders.drop_duplicates()
items = items.drop_duplicates()
products = products.drop_duplicates()
payments = payments.drop_duplicates()
categories = categories.drop_duplicates()


# -----------------------------
# LOAD INTO SQLITE
# -----------------------------

connection = sqlite3.connect(DB)

customers.to_sql("customers", connection, if_exists="replace", index=False)
orders.to_sql("orders", connection, if_exists="replace", index=False)
items.to_sql("order_items", connection, if_exists="replace", index=False)
products.to_sql("products", connection, if_exists="replace", index=False)
payments.to_sql("payments", connection, if_exists="replace", index=False)
categories.to_sql("category_translation", connection, if_exists="replace", index=False)


# -----------------------------
# CREATE USEFUL INDEXES
# -----------------------------

connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_orders_order_id ON orders(order_id)"
)

connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_items_order_id ON order_items(order_id)"
)

connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_items_product_id ON order_items(product_id)"
)

connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id)"
)

connection.commit()
connection.close()


print("ETL COMPLETE")
print(f"Customers: {len(customers):,}")
print(f"Delivered orders: {len(orders):,}")
print(f"Order items: {len(items):,}")
print(f"Products: {len(products):,}")
print(f"Payments: {len(payments):,}")
print(f"Database created: {DB}")

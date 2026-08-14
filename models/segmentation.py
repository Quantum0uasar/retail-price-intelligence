import sqlite3
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DB = "database/retail.db"

con = sqlite3.connect(DB)

query = """
SELECT
    c.customer_unique_id,
    MAX(o.order_purchase_timestamp) AS last_purchase,
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(oi.price) AS monetary
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
"""

df = pd.read_sql_query(query, con)
con.close()

df["last_purchase"] = pd.to_datetime(df["last_purchase"])

reference_date = df["last_purchase"].max() + pd.Timedelta(days=1)

df["recency"] = (
    reference_date - df["last_purchase"]
).dt.days

rfm = df[
    ["customer_unique_id", "recency", "frequency", "monetary"]
].copy()

# Reduce extreme differences between customers
rfm["frequency_log"] = np.log1p(rfm["frequency"])
rfm["monetary_log"] = np.log1p(rfm["monetary"])

features = rfm[
    ["recency", "frequency_log", "monetary_log"]
]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Create 4 customer groups
model = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["segment"] = model.fit_predict(scaled_features)

rfm.to_csv(
    "data/processed/customer_segments.csv",
    index=False
)

summary = (
    rfm.groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_spend=("monetary", "mean")
    )
    .round(2)
)

print(summary)

print("\nSaved to data/processed/customer_segments.csv")

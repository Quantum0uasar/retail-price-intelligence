import sqlite3
import numpy as np
import pandas as pd
import statsmodels.api as sm

DB = "database/retail.db"

con = sqlite3.connect(DB)

query = """
SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name
    ) AS category,
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    AVG(oi.price) AS avg_price,
    COUNT(*) AS quantity
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE oi.price > 0
GROUP BY category, month
"""

df = pd.read_sql_query(query, con)
con.close()

results = []

for category, group in df.groupby("category"):

    # Need enough months to make the regression useful
    if len(group) < 6:
        continue

    if group["avg_price"].nunique() < 2:
        continue

    group = group.copy()

    group["log_price"] = np.log(group["avg_price"])
    group["log_quantity"] = np.log(group["quantity"])

    X = sm.add_constant(group["log_price"])
    y = group["log_quantity"]

    model = sm.OLS(y, X).fit()

    results.append({
        "category": category,
        "elasticity": model.params["log_price"],
        "r_squared": model.rsquared,
        "p_value": model.pvalues["log_price"],
        "months": len(group)
    })

results_df = pd.DataFrame(results)

results_df = results_df.sort_values("elasticity")

results_df.to_csv(
    "data/processed/elasticity_results.csv",
    index=False
)

print(results_df.head(15).round(3))
print("\nSaved to data/processed/elasticity_results.csv")

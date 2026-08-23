from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "retail.db"
OUTPUT_DIR = BASE_DIR / "data" / "tableau"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_query(connection, query, output_name):
    df = pd.read_sql_query(query, connection)
    output_path = OUTPUT_DIR / output_name
    df.to_csv(output_path, index=False)
    print(f"Exported {output_name} ({len(df)} rows)")


def main():
    conn = sqlite3.connect(DB_PATH)

    monthly_revenue_query = """
    SELECT
        strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        SUM(oi.price) AS total_revenue,
        AVG(oi.price) AS avg_item_price,
        SUM(oi.freight_value) AS total_freight
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
    ORDER BY order_month;
    """

    category_performance_query = """
    SELECT
        p.product_category_name,
        COUNT(*) AS units_sold,
        SUM(oi.price) AS total_revenue,
        AVG(oi.price) AS avg_price,
        SUM(oi.freight_value) AS total_freight
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
    ORDER BY total_revenue DESC;
    """

    export_query(conn, monthly_revenue_query, "monthly_revenue.csv")
    export_query(conn, category_performance_query, "category_performance.csv")
    elasticity_df = pd.read_csv(BASE_DIR / "data" / "processed" / "elasticity_results.csv")
    elasticity_df.to_csv(OUTPUT_DIR / "elasticity_results.csv", index=False)

    segments_df = pd.read_csv(BASE_DIR / "data" / "processed" / "customer_segments.csv")
    segments_df.to_csv(OUTPUT_DIR / "customer_segments.csv", index=False)
    conn.close()


if __name__ == "__main__":
    main()

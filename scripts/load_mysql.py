"""Load the processed sales CSV into MySQL without storing credentials in code."""
from pathlib import Path
import os

import pandas as pd
import mysql.connector
from mysql.connector import Error

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "processed" / "clean_sales_data.csv"

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "sales_analytics"),
}

INSERT_SQL = """
INSERT INTO sales (
  order_id, order_date, customer_id, customer_name, region, product_id,
  product_name, category, quantity, unit_price, cost, discount,
  revenue, profit, profit_margin
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
  customer_name=VALUES(customer_name), region=VALUES(region),
  product_name=VALUES(product_name), category=VALUES(category),
  quantity=VALUES(quantity), unit_price=VALUES(unit_price), cost=VALUES(cost),
  discount=VALUES(discount), revenue=VALUES(revenue), profit=VALUES(profit),
  profit_margin=VALUES(profit_margin);
"""


def main() -> None:
    if not CSV_FILE.exists():
        raise FileNotFoundError("Run scripts/clean_data.py before loading MySQL.")
    if not MYSQL_CONFIG["password"]:
        raise ValueError("Set the MYSQL_PASSWORD environment variable before running.")

    df = pd.read_csv(CSV_FILE)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"]).dt.date
    rows = list(df.itertuples(index=False, name=None))
    connection = None
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        cursor.executemany(INSERT_SQL, rows)
        connection.commit()
        print(f"Loaded {cursor.rowcount} row operation(s) into sales_analytics.sales.")
        cursor.close()
    except Error as exc:
        if connection:
            connection.rollback()
        raise RuntimeError(f"MySQL load failed: {exc}") from exc
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()

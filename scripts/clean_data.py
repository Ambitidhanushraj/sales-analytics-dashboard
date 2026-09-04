"""Profile, clean, validate, and enrich the raw sales dataset."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "raw" / "sales_data.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "clean_sales_data.csv"
REJECTED_FILE = ROOT / "data" / "processed" / "rejected_sales_data.csv"

REQUIRED_COLUMNS = [
    "Order_ID", "Order_Date", "Customer_ID", "Customer_Name", "Region",
    "Product_ID", "Product_Name", "Category", "Quantity", "Unit_Price",
    "Cost", "Discount",
]


def profile(df: pd.DataFrame, label: str) -> None:
    print(f"\n--- {label} profile ---")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    print("Missing values:\n", df.isna().sum().to_string())
    print(f"Exact duplicate rows: {df.duplicated().sum()}")


def clean_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    data = df[REQUIRED_COLUMNS].copy().drop_duplicates()
    text_cols = ["Order_ID", "Customer_ID", "Customer_Name", "Region",
                 "Product_ID", "Product_Name", "Category"]
    for col in text_cols:
        data[col] = data[col].astype("string").str.strip()

    data["Region"] = data["Region"].str.title()
    data["Customer_Name"] = data["Customer_Name"].fillna("Unknown Customer")
    data["Category"] = data["Category"].fillna("Uncategorized")
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce").fillna(0)
    for col in ["Quantity", "Unit_Price", "Cost"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    # dayfirst=True handles the included DD-MM-YYYY sample while ISO dates remain stable.
    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"], errors="coerce", format="mixed", dayfirst=True
    )

    invalid = (
        data[["Order_ID", "Customer_ID", "Product_ID"]].isna().any(axis=1)
        | data["Order_Date"].isna()
        | data["Quantity"].isna() | (data["Quantity"] <= 0)
        | data["Unit_Price"].isna() | (data["Unit_Price"] <= 0)
        | data["Cost"].isna() | (data["Cost"] < 0)
        | ~data["Discount"].between(0, 1)
    )
    rejected = data.loc[invalid].copy()
    clean = data.loc[~invalid].copy()

    clean["Revenue"] = clean["Quantity"] * clean["Unit_Price"] * (1 - clean["Discount"])
    clean["Profit"] = clean["Revenue"] - clean["Quantity"] * clean["Cost"]
    clean["Profit_Margin"] = np.where(clean["Revenue"] != 0, clean["Profit"] / clean["Revenue"], 0)
    for col in ["Unit_Price", "Cost", "Discount", "Revenue", "Profit", "Profit_Margin"]:
        clean[col] = clean[col].round(2 if col not in ["Discount", "Profit_Margin"] else 4)
    clean["Order_Date"] = clean["Order_Date"].dt.strftime("%Y-%m-%d")
    clean = clean.sort_values(["Order_Date", "Order_ID"]).reset_index(drop=True)
    return clean, rejected


def validate(clean: pd.DataFrame) -> None:
    assert not clean.empty, "No valid rows remain after cleaning"
    assert clean["Order_ID"].notna().all(), "Order IDs cannot be missing"
    assert (clean["Quantity"] > 0).all(), "Quantity must be positive"
    assert (clean[["Unit_Price", "Cost"]] >= 0).all().all(), "Prices/costs cannot be negative"
    assert clean["Discount"].between(0, 1).all(), "Discount must be between 0 and 1"
    assert np.isfinite(clean[["Revenue", "Profit", "Profit_Margin"]]).all().all()


def main() -> int:
    try:
        raw = pd.read_csv(INPUT_FILE)
        profile(raw, "Raw data")
        clean, rejected = clean_sales(raw)
        validate(clean)
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        clean.to_csv(OUTPUT_FILE, index=False)
        rejected.to_csv(REJECTED_FILE, index=False)
        profile(clean, "Clean data")
        print(f"\nSaved {len(clean)} clean rows to {OUTPUT_FILE}")
        print(f"Saved {len(rejected)} rejected rows to {REJECTED_FILE}")
        return 0
    except (FileNotFoundError, ValueError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

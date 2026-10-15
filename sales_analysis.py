
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Project folders and files
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Create a sample dataset if one does not exist
if not DATA_FILE.exists():
    data = [
        ("2026-01-05", "Laptop", "Electronics", "West", 2, 55000),
        ("2026-01-12", "Headphones", "Electronics", "North", 10, 1500),
        ("2026-01-18", "Chair", "Furniture", "South", 5, 4500),
        ("2026-02-03", "Desk", "Furniture", "East", 3, 8000),
        ("2026-02-10", "Phone", "Electronics", "West", 4, 22000),
        ("2026-02-21", "Notebook", "Stationery", "North", 30, 80),
        ("2026-03-02", "Laptop", "Electronics", "South", 3, 55000),
        ("2026-03-11", "Pen", "Stationery", "East", 50, 20),
        ("2026-03-19", "Chair", "Furniture", "West", 7, 4500),
        ("2026-04-04", "Phone", "Electronics", "North", 6, 22000),
        ("2026-04-13", "Desk", "Furniture", "South", 4, 8000),
        ("2026-04-24", "Headphones", "Electronics", "East", 15, 1500),
        ("2026-05-06", "Laptop", "Electronics", "East", 2, 55000),
        ("2026-05-15", "Notebook", "Stationery", "West", 40, 80),
        ("2026-05-22", "Phone", "Electronics", "South", 5, 22000),
        ("2026-06-01", "Chair", "Furniture", "North", 8, 4500),
        ("2026-06-12", "Desk", "Furniture", "West", 5, 8000),
        ("2026-06-20", "Pen", "Stationery", "South", 70, 20),
        ("2026-07-03", "Laptop", "Electronics", "North", 4, 55000),
        ("2026-07-14", "Headphones", "Electronics", "West", 20, 1500),
        ("2026-07-23", "Chair", "Furniture", "East", 6, 4500),
        ("2026-08-05", "Phone", "Electronics", "East", 7, 22000),
        ("2026-08-16", "Desk", "Furniture", "North", 3, 8000),
        ("2026-08-25", "Notebook", "Stationery", "South", 60, 80),
        ("2026-09-04", "Laptop", "Electronics", "West", 3, 55000),
        ("2026-09-13", "Pen", "Stationery", "North", 90, 20),
        ("2026-09-21", "Phone", "Electronics", "South", 8, 22000),
        ("2026-10-02", "Chair", "Furniture", "East", 9, 4500),
        ("2026-10-09", "Headphones", "Electronics", "North", 25, 1500),
        ("2026-10-12", "Laptop", "Electronics", "South", 2, 55000),
    ]

    df_sample = pd.DataFrame(
        data,
        columns=[
            "Order_Date", "Product", "Category",
            "Region", "Quantity", "Unit_Price"
        ],
    )
    df_sample.to_csv(DATA_FILE, index=False)
    print("Sample sales dataset created.")

# 2. Load and clean the data
df = pd.read_csv(DATA_FILE)
required_columns = [
    "Order_Date", "Product", "Category",
    "Region", "Quantity", "Unit_Price"
]

missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in CSV: {sorted(missing)}")

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

df = df.dropna(subset=required_columns).copy()
df = df.drop_duplicates()
df = df[
    (df["Quantity"] >= 0) &
    (df["Unit_Price"] >= 0)
].copy()

if df.empty:
    raise ValueError("No valid sales records found.")

df["Sales"] = df["Quantity"] * df["Unit_Price"]
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# 3. Calculate business KPIs
total_revenue = df["Sales"].sum()
total_orders = len(df)
units_sold = df["Quantity"].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()
product_sales = df.groupby("Product")["Sales"].sum().sort_values(
    ascending=False
)
category_sales = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)
region_sales = df.groupby("Region")["Sales"].sum().sort_values(
    ascending=False
)

# 4. Display the results
print("\n===== SALES PERFORMANCE REPORT =====")
print(f"Total revenue:       Rs. {total_revenue:,.2f}")
print(f"Number of orders:    {total_orders}")
print(f"Units sold:          {units_sold:,.0f}")
print(f"Average order value: Rs. {average_order_value:,.2f}")

print("\nMonthly Sales:")
print(monthly_sales.to_string())

print("\nSales by Product:")
print(product_sales.to_string())

print("\nSales by Category:")
print(category_sales.to_string())

print("\nSales by Region:")
print(region_sales.to_string())

print("\nTop product:", product_sales.index[0])
print("Top category:", category_sales.index[0])
print("Top region:", region_sales.index[0])

# 5. Create charts
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="bar", title="Monthly Sales Performance")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_sales.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
product_sales.sort_values().plot(kind="barh", title="Sales by Product")
plt.xlabel("Revenue (Rs.)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "product_sales.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
category_sales.plot(
    kind="pie", autopct="%1.1f%%", startangle=90,
    title="Revenue Share by Category"
)
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_sales.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
region_sales.sort_values().plot(kind="barh", title="Sales by Region")
plt.xlabel("Revenue (Rs.)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "region_sales.png", dpi=150)
plt.close()

# 6. Export summary tables
monthly_sales.rename("Revenue").to_csv(
    OUTPUT_DIR / "monthly_sales_summary.csv"
)
product_sales.rename("Revenue").to_csv(
    OUTPUT_DIR / "product_sales_summary.csv"
)
category_sales.rename("Revenue").to_csv(
    OUTPUT_DIR / "category_sales_summary.csv"
)
region_sales.rename("Revenue").to_csv(
    OUTPUT_DIR / "region_sales_summary.csv"
)

# 7. Write a business insights report
best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()

report = f"""SALES PERFORMANCE ANALYSIS
===========================

Dataset records analyzed: {len(df)}
Total revenue: Rs. {total_revenue:,.2f}
Total orders: {total_orders}
Units sold: {units_sold:,.0f}
Average order value: Rs. {average_order_value:,.2f}

KEY FINDINGS
------------
Top product by revenue: {product_sales.index[0]}
Top category by revenue: {category_sales.index[0]}
Top region by revenue: {region_sales.index[0]}
Best month by revenue: {best_month}
Lowest month by revenue: {worst_month}

BUSINESS RECOMMENDATIONS
------------------------
1. Investigate what drives sales in the leading product category.
2. Review marketing and sales activity in the top-performing region.
3. Compare the strongest and weakest months to identify seasonal patterns.
4. Review product-level revenue before making inventory decisions.

Note: This project uses sample data for demonstration.
Revenue is not profit because product costs and expenses are not included.
"""

(OUTPUT_DIR / "business_insights.txt").write_text(
    report, encoding="utf-8"
)

print("\nAnalysis complete!")
print("Charts, summary tables and report saved in the outputs folder.")

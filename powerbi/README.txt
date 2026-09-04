POWER BI FILE
Save the finished report here as: sales_analytics_dashboard.pbix

Data connection:
1. Use MySQL database "sales_analytics" and table "sales"; or import
   data/processed/clean_sales_data.csv for a file-only prototype.
2. Confirm Order_Date is Date, IDs/names are Text, Quantity is Whole Number,
   money columns are Decimal/Currency, and Discount/Profit_Margin are Percentage.

Suggested DAX measures:
Total Revenue = SUM(sales[revenue])
Total Profit = SUM(sales[profit])
Total Orders = DISTINCTCOUNT(sales[order_id])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
Units Sold = SUM(sales[quantity])

Suggested report page:
- KPI cards: Total Revenue, Total Profit, Total Orders, Average Order Value,
  Profit Margin %
- Line chart: Total Revenue by Order_Date (month)
- Bar charts: Revenue by Region; Revenue and Profit by Category
- Top-products table: Product Name, Units Sold, Total Revenue, Total Profit
- Customer table: Customer Name, Total Orders, Total Revenue
- Slicers: Date, Region, Category

Validate the Power BI totals against sql/analysis_queries.sql before publishing.

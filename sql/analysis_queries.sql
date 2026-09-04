USE sales_analytics;

-- Executive KPIs
SELECT ROUND(SUM(revenue), 2) AS total_revenue,
       ROUND(SUM(profit), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders,
       ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
       ROUND(100 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales;

-- Monthly trend
SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
       ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales GROUP BY sales_month ORDER BY sales_month;

-- Region performance
SELECT region, ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit,
       ROUND(100 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS margin_pct
FROM sales GROUP BY region ORDER BY revenue DESC;

-- Category performance
SELECT category, SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales GROUP BY category ORDER BY revenue DESC;

-- Top 10 products
SELECT product_id, product_name, category, SUM(quantity) AS units_sold,
       ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit
FROM sales GROUP BY product_id, product_name, category
ORDER BY revenue DESC LIMIT 10;

-- Top customers
SELECT customer_id, customer_name, COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(revenue), 2) AS revenue, ROUND(SUM(profit), 2) AS profit
FROM sales GROUP BY customer_id, customer_name ORDER BY revenue DESC LIMIT 10;

-- Discount bands and profitability
SELECT CASE WHEN discount = 0 THEN 'No discount'
            WHEN discount <= 0.05 THEN '1-5%'
            WHEN discount <= 0.10 THEN '6-10%'
            ELSE 'Above 10%' END AS discount_band,
       COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit
FROM sales GROUP BY discount_band ORDER BY MIN(discount);

-- Loss-making orders
SELECT order_id, order_date, product_name, revenue, profit, profit_margin
FROM sales WHERE profit < 0 ORDER BY profit;

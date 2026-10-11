-- Run after loading data into the target warehouse.

-- 1. Duplicate sale IDs (expect zero rows)
SELECT sale_id, COUNT(*) AS row_count
FROM fact_sales
GROUP BY sale_id
HAVING COUNT(*) > 1;

-- 2. Invalid quantity or price (expect zero rows)
SELECT *
FROM fact_sales
WHERE quantity <= 0 OR unit_price < 0 OR line_total < 0;

-- 3. Reconcile total amount
SELECT COUNT(*) AS sales_count, SUM(line_total) AS gross_sales
FROM fact_sales;

-- 4. Sales by day
SELECT order_date, COUNT(*) AS order_lines, SUM(line_total) AS daily_sales
FROM fact_sales
GROUP BY order_date
ORDER BY order_date;

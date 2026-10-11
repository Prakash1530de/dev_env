-- Example PostgreSQL warehouse DDL.
-- Adapt types and syntax for your target database.

CREATE TABLE IF NOT EXISTS dim_product (
    product_id   VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category     VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id      VARCHAR(50) PRIMARY KEY,
    order_date   DATE NOT NULL,
    customer_id  VARCHAR(50) NOT NULL,
    product_id   VARCHAR(50) NOT NULL REFERENCES dim_product(product_id),
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    unit_price   NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    line_total   NUMERIC(14, 2) NOT NULL,
    loaded_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id ON fact_sales(customer_id);

CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

CREATE TABLE IF NOT EXISTS sales (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(30) NOT NULL,
    customer_name VARCHAR(120) NOT NULL,
    region VARCHAR(50) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    product_name VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    cost DECIMAL(12,2) NOT NULL,
    discount DECIMAL(6,4) NOT NULL DEFAULT 0,
    revenue DECIMAL(14,2) NOT NULL,
    profit DECIMAL(14,2) NOT NULL,
    profit_margin DECIMAL(8,4) NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (quantity > 0),
    CHECK (unit_price > 0),
    CHECK (cost >= 0),
    CHECK (discount BETWEEN 0 AND 1),
    INDEX idx_sales_date (order_date),
    INDEX idx_sales_region (region),
    INDEX idx_sales_category (category),
    INDEX idx_sales_customer (customer_id)
);

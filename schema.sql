-- Customer & Order Management API: database schema (MySQL 8)
-- Run once:  mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS customer_order_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE customer_order_db;

-- customers
CREATE TABLE IF NOT EXISTS customers (
    id         INT          NOT NULL AUTO_INCREMENT,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL,
    phone      VARCHAR(15)  NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- orders  (customers 1 ---- N orders)
-- No ON DELETE CASCADE on purpose: deleting a customer who still has
-- orders is rejected by MySQL and the API returns 409.
CREATE TABLE IF NOT EXISTS orders (
    id           INT           NOT NULL AUTO_INCREMENT,
    customer_id  INT           NOT NULL,
    order_number VARCHAR(50)   NOT NULL,
    amount       DECIMAL(10,2) NOT NULL,
    status       VARCHAR(30)   NOT NULL,
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (id),
    INDEX idx_orders_customer_id (customer_id)
) ENGINE=InnoDB;


-- 1. Revenue by category
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name) AS category,
    COUNT(*) AS units_sold,
    ROUND(AVG(oi.price), 2) AS average_price,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;


-- 2. Monthly sales trend
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;


-- 3. Price range by category
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name) AS category,
    ROUND(MIN(oi.price), 2) AS minimum_price,
    ROUND(AVG(oi.price), 2) AS average_price,
    ROUND(MAX(oi.price), 2) AS maximum_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY category
ORDER BY average_price DESC
LIMIT 10;


-- 4. Freight burden by category
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name) AS category,
    ROUND(AVG(oi.freight_value), 2) AS average_freight,
    ROUND(AVG(oi.price), 2) AS average_price,
    ROUND(AVG(oi.freight_value / oi.price) * 100, 2) AS freight_percent
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE oi.price > 0
GROUP BY category
ORDER BY freight_percent DESC
LIMIT 10;


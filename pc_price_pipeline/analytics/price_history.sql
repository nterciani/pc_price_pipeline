-- Provides a view with the historical prices for every product and retailer combination.
CREATE OR REPLACE VIEW `pc-price-pipeline.powerbi_reports.price_history` AS
SELECT
    DATE(fp.price_date) AS price_day,
    fp.product_key,
    dp.product_name,
    dp.product_brand,
    fp.product_category,
    fp.retailer_key,
    dr.retailer_name,
    dr.retailer_domain,
    dr.retailer_country,
    MIN(fp.price) AS price
FROM `pc-price-pipeline.pc_part_prices_star.fact_prices` AS fp
LEFT JOIN `pc-price-pipeline.pc_part_prices_star.dim_products` AS dp
    ON fp.product_key = dp.product_key
LEFT JOIN `pc-price-pipeline.pc_part_prices_star.dim_retailers` AS dr
    ON fp.retailer_key = dr.retailer_key
GROUP BY
    DATE(fp.price_date),
    fp.product_key,
    dp.product_name,
    dp.product_brand,
    fp.product_category,
    fp.retailer_key,
    dr.retailer_name,
    dr.retailer_domain,
    dr.retailer_country;
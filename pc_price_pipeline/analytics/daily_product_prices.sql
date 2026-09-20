-- Provides a table with the latest two days of product prices for every product and 
-- retailer combination. This allows for latest price drop analysis.
CREATE OR REPLACE TABLE
  `pc-price-pipeline.powerbi_reports.daily_product_prices`
CLUSTER BY product_key, retailer_key
AS
WITH daily_prices AS (
    SELECT
        DATE(fp.price_date) AS price_day,
        fp.product_key,
        fp.retailer_key,
        fp.product_category,
        MIN(fp.price) AS min_price
    FROM `pc-price-pipeline.pc_part_prices_star.fact_prices` AS fp
    GROUP BY
        price_day,
        fp.product_key,
        fp.retailer_key,
        fp.product_category
),

ranked_days AS (
    SELECT
        daily_prices.*,
        ROW_NUMBER() OVER (
            PARTITION BY product_key, retailer_key
            ORDER BY price_day DESC
        ) AS day_rank
    FROM daily_prices
)

SELECT
    dp.product_key,
    dp.product_name,
    dp.product_brand,
    rd.price_day,
    rd.retailer_key,
    rd.product_category,
    rd.min_price
FROM ranked_days AS rd
LEFT JOIN `pc-price-pipeline.pc_part_prices_star.dim_products` AS dp
    ON rd.product_key = dp.product_key
WHERE rd.day_rank <= 2;
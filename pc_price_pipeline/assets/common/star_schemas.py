RAW_PRICES_SCHEMA = [
    {"name": "raw_name", "type": "STRING"},
    {"name": "raw_price", "type": "FLOAT"},
    {"name": "store", "type": "STRING"},
    {"name": "category", "type": "STRING"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

FACT_PRICES_SCHEMA = [
    {"name": "price_date", "type": "TIMESTAMP"},
    {"name": "product_key", "type": "STRING"},
    {"name": "retailer_key", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "source_url", "type": "STRING"},
]

FACT_VECTOR_SEARCH_SCHEMA = [
    {"name": "product_key", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "match_confidence", "type": "FLOAT"},
    {"name": "match_method", "type": "STRING"},
    {"name": "is_approved", "type": "BOOLEAN"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
]

DIM_PRODUCTS_SCHEMA = [
    {"name": "product_key", "type": "STRING"},
    {"name": "product_embedding", "type": "FLOAT64", "mode": "REPEATED"},
    {"name": "product_name", "type": "STRING"},
    {"name": "product_brand", "type": "STRING"},
    {"name": "product_category", "type": "STRING"},
]

DIM_RETAILERS_SCHEMA = [
    {"name": "retailer_key", "type": "STRING"}, # ex: bestbuy_us, bestbuy_ca
    {"name": "retailer_name", "type": "STRING"}, # ex: Best Buy
    {"name": "retailer_domain", "type": "STRING"}, # ex: bestbuy.com, bestbuy.ca
    {"name": "retailer_country", "type": "STRING"}, # ex: US, CA
]

DIM_CPU_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "socket", "type": "STRING"},
    {"name": "core_count", "type": "STRING"},
    {"name": "core_clock", "type": "STRING"},
    {"name": "thread_count", "type": "STRING"},
    {"name": "integrated_graphics", "type": "STRING"},
    {"name": "tdp", "type": "STRING"},
    {"name": "needs_review", "type": "BOOL"},
]

DIM_GPU_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "model_line", "type": "STRING"},
    {"name": "chipset", "type": "STRING"},
    {"name": "memory", "type": "STRING"},
    {"name": "memory_type", "type": "STRING"},
    {"name": "overclocked", "type": "BOOL"},
    {"name": "needs_review", "type": "BOOL"},
]

DIM_MEMORY_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "model_line", "type": "STRING"},
    {"name": "memory_type", "type": "STRING"},
    {"name": "capacity", "type": "STRING"},
    {"name": "speed", "type": "STRING"},
    {"name": "modules", "type": "STRING"},
    {"name": "cas_latency", "type": "STRING"},
    {"name": "color", "type": "STRING"},
    {"name": "needs_review", "type": "BOOL"},
]

DIM_MOTHERBOARD_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "model_line", "type": "STRING"},
    {"name": "socket", "type": "STRING"},
    {"name": "form_factor", "type": "STRING"},
    {"name": "chipset", "type": "STRING"},
    {"name": "memory_type", "type": "STRING"},
    {"name": "wifi", "type": "BOOL"},
    {"name": "needs_review", "type": "BOOL"},
]

DIM_STORAGE_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "model_line", "type": "STRING"},
    {"name": "capacity", "type": "STRING"},
    {"name": "storage_type", "type": "STRING"},
    {"name": "form_factor", "type": "STRING"},
    {"name": "heatsink", "type": "BOOL"},
    {"name": "interface", "type": "STRING"},
    {"name": "needs_review", "type": "BOOL"},
]

DIM_PSU_SPECS = [
    {"name": "product_key", "type": "STRING"},
    {"name": "model_line", "type": "STRING"},
    {"name": "psu_type", "type": "STRING"},
    {"name": "wattage", "type": "STRING"},
    {"name": "modular", "type": "BOOL"},
    {"name": "efficiency_rating", "type": "STRING"},
    {"name": "color", "type": "STRING"},
    {"name": "needs_review", "type": "BOOL"},
]
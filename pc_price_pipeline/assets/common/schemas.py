RAW_TABLE_SCHEMA = [
    {"name": "raw_name", "type": "STRING"},
    {"name": "raw_price", "type": "FLOAT"},
    {"name": "store", "type": "STRING"},
    {"name": "category", "type": "STRING"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

FACT_PARTS_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_CPUS_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "socket", "type": "STRING"}, # AM4, AM5, LGA1700
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_GPUS_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "chipset", "type": "STRING"}, # GeForce RTX 4060, Radeon RX 9060 XT
    {"name": "memory", "type": "STRING"}, # 16GB, 8GB, 32GB
    {"name": "memory_type", "type": "STRING"}, # GDDR5, GDDR5X, GDDR6
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_MOBOS_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "socket", "type": "STRING"}, # AM4, AM5, LGA1700
    {"name": "form_factor", "type": "STRING"}, # ATX, EATX, Micro ATX
    {"name": "chipset", "type": "STRING"}, # AMD B550/B650/X870E, Intel B560
    {"name": "memory_type", "type": "STRING"}, # DDR4, DDR5
    {"name": "wifi", "type": "BOOL"},
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_MEMORY_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "memory_type", "type": "STRING"}, # DDR5, DDR4
    {"name": "capacity", "type": "STRING"}, # 16GB, 32GB, 64GB
    {"name": "speed", "type": "STRING"}, # 6000, 3200, 5600
    {"name": "modules", "type": "STRING"}, # 2 x 16GB, 1 x 32GB
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_STORAGE_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "capacity", "type": "STRING"}, # 2 TB, 512 GB
    {"name": "storage_type", "type": "STRING"}, # SSD, HDD
    {"name": "form_factor", "type": "STRING"}, # M.2-2280, 2.5"
    {"name": "interface", "type": "STRING"},  # PCIe 4.0 X4, 5.0 X2, SATA 6.0 Gb/s
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

ENRICHED_PSU_SCHEMA = [
    {"name": "product_id", "type": "STRING"},
    {"name": "raw_name", "type": "STRING"},
    {"name": "product_family", "type": "STRING"},
    {"name": "brand", "type": "STRING"},
    {"name": "psu_type", "type": "STRING"}, # ATX, SFX
    {"name": "efficiency_rating", "type": "STRING"}, # 80+ Gold, 80+ Bronze
    {"name": "wattage", "type": "STRING"}, # 750 W, 1000 W
    {"name": "modular", "type": "BOOL"},
    {"name": "category", "type": "STRING"},
    {"name": "store", "type": "STRING"},
    {"name": "price", "type": "FLOAT"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "source_url", "type": "STRING"},
]

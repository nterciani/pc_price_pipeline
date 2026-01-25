from pc_price_pipeline.assets.common.schemas import *

def test_enriched_cpu_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_CPUS_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "socket",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

def test_enriched_gpu_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_GPUS_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "chipset",
        "memory",
        "memory_type",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

def test_enriched_mobo_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_MOBOS_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "socket",
        "form_factor",
        "chipset",
        "memory_type",
        "wifi",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

def test_enriched_memory_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_MEMORY_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "memory_type",
        "capacity",
        "speed",
        "modules",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

def test_enriched_storage_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_STORAGE_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "capacity",
        "storage_type",
        "form_factor",
        "interface",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

def test_enriched_psu_schema_order():
    schema_columns = [col["name"] for col in ENRICHED_PSU_SCHEMA]

    assert schema_columns == [
        "product_id",
        "raw_name",
        "product_family",
        "brand",
        "psu_type",
        "efficiency_rating",
        "wattage",
        "modular",
        "category",
        "store",
        "price",
        "scraped_at",
        "source_url",
    ]

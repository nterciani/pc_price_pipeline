import pandas as pd
from pc_price_pipeline.assets.cpu.enriched import enriched_cpus
from pc_price_pipeline.assets.common.schemas import ENRICHED_CPUS_SCHEMA as schema


def _dummy_value_for_type(field_type: str):
    if field_type == "FLOAT":
        return 0.0
    if field_type == "TIMESTAMP":
        return "2026-01-01T00:00:00"
    if field_type == "BOOL":
        return False
    return "DUMMY"


def _make_rows_with_schema_defaults(raw_names):
    defaults = {
        col["name"]: _dummy_value_for_type(col["type"])
        for col in schema
    }
    return [{**defaults, "raw_name": value} for value in raw_names]


def test_enriched_cpus_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "AMD Ryzen 3 4100 - Ryzen 3 4000 Series Renoir (Zen 2) Quad-Core 3.8 GHz Socket AM4 65W None Integrated Graphics Desktop CPU Processor",
            "AMD Ryzen 7 5800XT - 8-Core 3.8 GHz Socket AM4 105W None Integrated Graphics Desktop CPU Processor",
            "Intel Core i9-14900KF - Core i9 14th Gen 24-Core (8P+16E) LGA 1700 125W None Integrated Graphics Processor",
        ],
        "category": ["CPU", "CPU", "CPU"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_cpus(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "AMD"
    assert row["socket"] == "AM4"
    assert row["product_family"] == "AMD RYZEN 3 4100"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "AMD"
    assert row2["socket"] == "AM4"
    assert row2["product_family"] == "AMD RYZEN 7 5800XT"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "INTEL"
    assert row3["socket"] == "LGA 1700"
    assert row3["product_family"] == "INTEL CORE I9 14900KF"
    assert isinstance(row3["product_id"], str)


def test_enriched_cpus_drops_null_product_family():
    raw_names = [
        'AMD Ryzen 7 5800X',
        '',
        None,
        12345,  # clearly wrong type
        'HPE AMD EPYC 9004 (4th Gen) 9224 Tetracosa-core (24 Core) 2.50 GHz Processor Upgrade - 64 MB L3 Cache',
    ]
    sample = pd.DataFrame(_make_rows_with_schema_defaults(raw_names))
    enriched = enriched_cpus(sample)

    # Product family should not be null or empty
    assert enriched['product_family'].isnull().sum() == 0
    assert (enriched['product_family'].str.strip() == '').sum() == 0

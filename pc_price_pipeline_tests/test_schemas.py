import pytest

from pc_price_pipeline.assets.common import star_schemas


SCHEMA_NAMES = [
    "RAW_PRICES_SCHEMA",
    "DIM_PRODUCTS_SCHEMA",
    "FACT_PRICES_SCHEMA",
    "FACT_VECTOR_SEARCH_SCHEMA",
    "DIM_CPU_SPECS",
    "DIM_GPU_SPECS",
    "DIM_MEMORY_SPECS",
    "DIM_MOTHERBOARD_SPECS",
    "DIM_STORAGE_SPECS",
    "DIM_PSU_SPECS",
]


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_current_schema_has_unique_named_columns(schema_name):
    schema = getattr(star_schemas, schema_name)
    names = [column["name"] for column in schema]

    assert names
    assert len(names) == len(set(names))
    assert all("type" in column for column in schema)


def test_fact_price_schema_contains_star_schema_keys():
    names = {column["name"] for column in star_schemas.FACT_PRICES_SCHEMA}

    assert {"price_date", "product_key", "retailer_key", "price"} <= names

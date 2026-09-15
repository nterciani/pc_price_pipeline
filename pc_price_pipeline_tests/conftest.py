import pandas as pd
import pytest


@pytest.fixture
def raw_listing():
    def make(raw_name, category, source_url="https://example.com/product"):
        return pd.DataFrame(
            {
                "raw_name": [raw_name],
                "raw_price": [100.0],
                "store": ["Newegg"],
                "category": [category],
                "scraped_at": [pd.Timestamp("2026-01-25 22:07:35", tz="UTC")],
                "source_url": [source_url],
            }
        )

    return make


@pytest.fixture
def expected_raw_columns():
    return ["raw_name", "raw_price", "store", "category", "scraped_at", "source_url"]


@pytest.fixture
def expected_fact_columns():
    return [
        "price_date",
        "product_key",
        "retailer_key",
        "product_category",
        "price",
        "source_url",
    ]

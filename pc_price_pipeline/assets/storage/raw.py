import pandas as pd
from dagster import asset
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category
from pc_price_pipeline.assets.common.star_schemas import RAW_PRICES_SCHEMA
from pc_price_pipeline.assets.common.bigquery_helpers import write_raw_to_bq

NEWEGG_STORAGE_INTERNAL_SSD = "https://www.newegg.ca/p/pl?N=100011700%204814%208000"
NEWEGG_STORAGE_INTERNAL_HDD = "https://www.newegg.ca/p/pl?N=100167537%204814%208000"

@asset(group_name="storage")
def raw_storage() -> pd.DataFrame:
    """
    Gathers raw storage pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    rows = []

    row_ssd = scrape_newegg_category("STORAGE", NEWEGG_STORAGE_INTERNAL_SSD)
    row_hdd = scrape_newegg_category("STORAGE", NEWEGG_STORAGE_INTERNAL_HDD)

    rows = row_ssd + row_hdd

    raw_df = pd.DataFrame(rows)

    write_raw_to_bq(raw_df, "pc_part_prices_star.raw_prices", RAW_PRICES_SCHEMA)

    return raw_df

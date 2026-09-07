import pandas as pd
from dagster import asset
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category
from pc_price_pipeline.assets.common.star_schemas import RAW_PRICES_SCHEMA
from pc_price_pipeline.assets.common.bigquery_helpers import write_raw_to_bq

NEWEGG_MEMORY = "https://www.newegg.ca/p/pl?N=100007610%204814%208000"

@asset(group_name="memory")
def raw_memory() -> pd.DataFrame:
    """
    Gathers raw memory pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    raw_df = pd.DataFrame(scrape_newegg_category("MEMORY", NEWEGG_MEMORY))

    write_raw_to_bq(raw_df, "pc_part_prices_star.raw_prices", RAW_PRICES_SCHEMA)

    return raw_df

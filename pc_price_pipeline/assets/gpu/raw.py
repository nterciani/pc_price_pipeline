import pandas as pd
from dagster import asset
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category
from pc_price_pipeline.assets.common.star_schemas import RAW_PRICES_SCHEMA
from pc_price_pipeline.assets.common.bigquery_helpers import write_raw_to_bq

NEWEGG_GPUS = "https://www.newegg.ca/p/pl?N=100007708%208000&ComboBundle=true"

@asset(group_name="gpus")
def raw_gpus() -> pd.DataFrame:
    """
    Gathers raw GPU pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    raw_df = pd.DataFrame(scrape_newegg_category("GPU", NEWEGG_GPUS))

    write_raw_to_bq(raw_df, "pc_part_prices_star.raw_prices", RAW_PRICES_SCHEMA)

    return raw_df

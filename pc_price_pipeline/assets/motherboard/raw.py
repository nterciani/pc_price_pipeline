import pandas as pd
from dagster import asset
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category
from pc_price_pipeline.assets.common.star_schemas import RAW_PRICES_SCHEMA
from pc_price_pipeline.assets.common.bigquery_helpers import write_star_to_bq

NEWEGG_AMD_MOTHERBOARDS = "https://www.newegg.ca/p/pl?N=100007624%20601413462%20601413455%208000&ComboBundle=true"
NEWEGG_INTEL_MOTHERBOARDS = "https://www.newegg.ca/p/pl?N=100007626%208000%20601413471%20601458446&ComboBundle=true"

@asset(group_name="motherboards")
def raw_motherboards() -> pd.DataFrame:
    """
    Gathers raw Motherboard pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    rows = []
    rows += scrape_newegg_category("MOTHERBOARD", NEWEGG_AMD_MOTHERBOARDS)
    rows += scrape_newegg_category("MOTHERBOARD", NEWEGG_INTEL_MOTHERBOARDS)

    raw_df = pd.DataFrame(rows)

    write_star_to_bq(raw_df, "pc_part_prices_star.raw_prices", RAW_PRICES_SCHEMA)

    return raw_df

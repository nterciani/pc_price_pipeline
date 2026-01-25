from dagster import asset
import pandas as pd
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category

NEWEGG_PSUS = "https://www.newegg.ca/p/pl?N=100007656%204814%208000"

@asset(group_name="psus")
def raw_psus() -> pd.DataFrame:
    """
    Gathers raw Power Supply Unit pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    return pd.DataFrame(scrape_newegg_category("PSU", NEWEGG_PSUS))

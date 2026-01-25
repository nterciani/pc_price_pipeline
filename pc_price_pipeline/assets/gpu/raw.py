from dagster import asset
import pandas as pd
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category

NEWEGG_GPUS = "https://www.newegg.ca/p/pl?N=100007708%208000&ComboBundle=true"

@asset(group_name="gpus")
def raw_gpus() -> pd.DataFrame:
    """
    Gathers raw GPU pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    return pd.DataFrame(scrape_newegg_category("GPU", NEWEGG_GPUS))

from dagster import asset
import pandas as pd
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category

NEWEGG_CPUS = "https://www.newegg.ca/p/pl?N=100007670%204814%208000&ComboBundle=true"

@asset(group_name="cpus")
def raw_cpus() -> pd.DataFrame:
    """
    Gathers raw CPU pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    return pd.DataFrame(scrape_newegg_category("CPU", NEWEGG_CPUS))

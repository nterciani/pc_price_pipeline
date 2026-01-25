from dagster import asset
import pandas as pd
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category

NEWEGG_AMD_MOBOS = "https://www.newegg.ca/p/pl?N=100007624%20601413462%20601413455%208000&ComboBundle=true"
NEWEGG_INTEL_MOBOS = "https://www.newegg.ca/p/pl?N=100007626%208000%20601413471%20601458446&ComboBundle=true"

@asset(group_name="mobos")
def raw_mobos() -> pd.DataFrame:
    """
    Gathers raw Motherboard pricing data scraped from online marketplaces.
    This data is unvalidated and may contain errors.
    """
    rows = []
    rows += scrape_newegg_category("MOTHERBOARD", NEWEGG_AMD_MOBOS)
    rows += scrape_newegg_category("MOTHERBOARD", NEWEGG_INTEL_MOBOS)

    return pd.DataFrame(rows)

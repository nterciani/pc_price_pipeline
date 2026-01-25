from dagster import asset
import pandas as pd
from pc_price_pipeline.scrapers.newegg import scrape_newegg_category

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
    for d in row_ssd:
        d["storage_type"] = "SSD"

    rows += row_ssd

    row_hdd = scrape_newegg_category("STORAGE", NEWEGG_STORAGE_INTERNAL_HDD)
    for d in row_hdd:
        d["storage_type"] = "HDD"

    rows += row_hdd

    df = pd.DataFrame(rows)

    return df

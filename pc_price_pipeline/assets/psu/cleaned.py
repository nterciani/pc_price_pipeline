from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df

@asset(group_name="psus")
def cleaned_psus(raw_psus: pd.DataFrame) -> pd.DataFrame:
    return cleaned_prices_df(raw_psus)

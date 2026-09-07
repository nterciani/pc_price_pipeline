import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df

@asset(group_name="gpus")
def cleaned_gpus(raw_gpus: pd.DataFrame) -> pd.DataFrame:
    return cleaned_prices_df(raw_gpus)

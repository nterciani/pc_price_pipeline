from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df

@asset(group_name="cpus")
def cleaned_cpus(raw_cpus: pd.DataFrame) -> pd.DataFrame:
    return cleaned_prices_df(raw_cpus)

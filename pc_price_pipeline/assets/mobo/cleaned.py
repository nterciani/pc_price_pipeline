from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df

@asset(group_name="mobos")
def cleaned_mobos(raw_mobos: pd.DataFrame) -> pd.DataFrame:
    return cleaned_prices_df(raw_mobos)

import pandas as pd
from pc_price_pipeline.assets.common.utils import *

def normalize_cpu_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["product_family"] = df["product_family"].apply(normalize_text)
    df["brand"] = df["brand"].apply(normalize_text)
    df["socket"] = df["socket"].apply(normalize_text)

    return df

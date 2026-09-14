import pandas as pd
from pc_price_pipeline.assets.common.utils import *


def normalize_cpu_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df["socket"] = df["socket"].apply(normalize_text)

    return df

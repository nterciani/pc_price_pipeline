import pandas as pd
from pc_price_pipeline.assets.common.utils import *

def normalize_memory_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)
    df.loc[df["brand"].str.contains("TEAM"), "brand"] = "TEAM GROUP"

    df["memory_type"] = df["memory_type"].apply(normalize_text)
    df["capacity"] = df["capacity"].apply(normalize_text).str.replace(' ', '')

    return df

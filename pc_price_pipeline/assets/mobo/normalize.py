import pandas as pd
from pc_price_pipeline.assets.common.utils import *

FORM_FACTOR_MAP = {"MATX": "MICRO ATX", "ITX": "MINI ITX"}

def normalize_mobo_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)
    df["socket"] = df["socket"].apply(normalize_text)

    df["form_factor"] = df["form_factor"].apply(normalize_text)
    df["form_factor"] = df["form_factor"].replace(FORM_FACTOR_MAP)

    df["chipset"] = df["chipset"].apply(normalize_text)
    df["memory_type"] = df["memory_type"].apply(normalize_text)

    return df

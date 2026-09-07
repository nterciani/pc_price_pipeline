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

def normalize_motherboard_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df["socket"] = df["socket"].apply(normalize_text)

    # backfall null form factors onto link
    df["form_factor"] = df["form_factor"].fillna(df["source_url"].str.extract(MOTHERBOARD_FORM_FACTOR_PATTERN).iloc[:, 0])

    df["form_factor"] = df["form_factor"].apply(normalize_text)
    df["form_factor"] = df["form_factor"].replace(FORM_FACTOR_MAP)

    df["chipset"] = df["chipset"].apply(normalize_text)
    df["memory_type"] = df["memory_type"].apply(normalize_text)

    invalid_model_line = df["model_line"].str.contains(r"(?i)(?:MOTHERBOARD)", na=False, regex=True)

    df.loc[invalid_model_line, "model_line"] = df.loc[invalid_model_line, "model_line"].str.split(r"(?i)(?:MOTHERBOARD)", n=1, regex=True).str[0].str.strip()
    df["model_line"] = df["model_line"].str.upper()

    return df
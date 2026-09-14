import pandas as pd
from pc_price_pipeline.assets.common.utils import *

FORM_FACTOR_MAP = {"MATX": "MICRO ATX", "ITX": "MINI ITX"}
MOTHERBOARD_MODEL_LINE_SUFFIX = r"(?i)\s+\bMOTHERBOARD\b.*$"
MOTHERBOARD_MEMORY_SUFFIX = r"(?i)\s+\bDDR\dX?\b.*$"
MOTHERBOARD_REVISION_SUFFIX = r"(?i)\s*\(REV\.?\s*[\d.]+\)\s*$"


def normalize_motherboard_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df["socket"] = df["socket"].apply(normalize_text)

    # backfall null form factors onto link
    df["form_factor"] = df["form_factor"].fillna(df["source_url"].str.extract(MOTHERBOARD_FORM_FACTOR_PATTERN).iloc[:, 0])

    df["form_factor"] = df["form_factor"].apply(normalize_text)
    df["form_factor"] = df["form_factor"].replace(FORM_FACTOR_MAP)

    df["chipset"] = df["chipset"].apply(normalize_text)
    df["memory_type"] = df["memory_type"].apply(normalize_text)

    df["model_line"] = df["model_line"].apply(normalize_text)
    df["model_line"] = df["model_line"].str.replace(MOTHERBOARD_REVISION_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(MOTHERBOARD_MODEL_LINE_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(MOTHERBOARD_MEMORY_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(r"\s*[,\-]+\s*$", "", regex=True)
    df["model_line"] = df["model_line"].str.replace(r"\s+", " ", regex=True).str.strip()

    return df

import pandas as pd
from pc_price_pipeline.assets.common.utils import *

INVALID_BRAND_OR_MODEL = r"(?i)(?:\d{2,4}(?:GB|MHZ))"
MEMORY_MODEL_LINE_GENERIC = r"(?i)\b(?:RAM MODULE|MEMORY|DDR\dX?L?|SDRAM|DRAM|RAM|MODULE|\d+GB|GROUP)\b"


def normalize_memory_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df.loc[df["product_brand"].str.contains("TEAM", na=False), "product_brand"] = "TEAM GROUP"

    df["memory_type"] = df["memory_type"].apply(normalize_text)
    df["capacity"] = df["capacity"].apply(normalize_text).str.replace(' ', '')
    df["modules"] = df["modules"].apply(normalize_text)
    df["speed"] = df["speed"].apply(normalize_text)
    df["model_line"] = df["model_line"].apply(normalize_text)
    df["color"] = df["color"].apply(normalize_text)

    # Backfill CAS latency from the URL when extraction produced a blank value.
    blank_cas_latency = df["cas_latency"].isna() | df["cas_latency"].eq("")
    df.loc[blank_cas_latency, "cas_latency"] = df.loc[
        blank_cas_latency, "source_url"
    ].str.extract(MEMORY_CAS_LATENCY_PATTERN).iloc[:, 0]
    df["cas_latency"] = df["cas_latency"].apply(normalize_text)

    # Get rid of unrealistic brand or model-line values.
    mask_invalid_brand = df["product_brand"].str.contains(INVALID_BRAND_OR_MODEL, na=False, regex=True)

    df.loc[mask_invalid_brand, "product_brand"] = df.loc[
        mask_invalid_brand, "raw_name"].str.replace(INVALID_BRAND_OR_MODEL, "", regex=True).str.strip().str.extract(MEMORY_BRAND_PATTERN).iloc[:, 0]

    df["model_line"] = df["model_line"].str.replace(MEMORY_MODEL_LINE_GENERIC, "", regex=True)
    df["model_line"] = df["model_line"].str.split(r"(?i)\s*\(FOR ", n=1, regex=True).str[0]
    df["model_line"] = df["model_line"].str.split(r"(?i)\s+FOR\s+", n=1, regex=True).str[0]
    df["model_line"] = df["model_line"].str.split(r"(?i)\s*SERIES", n=1, regex=True).str[0]
    df["model_line"] = df["model_line"].str.replace(r"\s+", " ", regex=True).str.strip()

    mask_invalid_model_line = df["model_line"].str.contains(INVALID_BRAND_OR_MODEL, na=False, regex=True)
    model_line_equals_brand = df["model_line"].eq(df["product_brand"])

    df.loc[mask_invalid_model_line | model_line_equals_brand, "model_line"] = None

    return df

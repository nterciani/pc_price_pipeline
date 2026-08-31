import pandas as pd
from pc_price_pipeline.assets.common.utils import *

INVALID_BRAND_OR_MODEL = r"(?i)(?:\d{2,4}(?:GB|MHZ))"

def normalize_memory_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)
    df.loc[df["brand"].str.contains("TEAM"), "brand"] = "TEAM GROUP"

    df["memory_type"] = df["memory_type"].apply(normalize_text)
    df["capacity"] = df["capacity"].apply(normalize_text).str.replace(' ', '')

    return df


def normalize_memory_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df.loc[df["product_brand"].str.contains("TEAM"), "product_brand"] = "TEAM GROUP"

    df["memory_type"] = df["memory_type"].apply(normalize_text)
    df["capacity"] = df["capacity"].apply(normalize_text).str.replace(' ', '')
    df["modules"] = df["modules"].apply(normalize_text)
    df["speed"] = df["speed"].apply(normalize_text)
    df['model_line'] = df['model_line'].apply(normalize_text)
    df['color'] = df['color'].apply(normalize_text)

    # cas latency backfall onto url
    df["cas_latency"] = df["cas_latency"].fillna(df["source_url"].str.extract(MEMORY_CAS_LATENCY_PATTERN).iloc[:, 0])
    df["cas_latency"] = df["cas_latency"].apply(normalize_text)


    # get rid of unrealistic brand or model-line values
    mask_invalid_brand = df["product_brand"].str.contains(INVALID_BRAND_OR_MODEL, na=False, regex=True)
    mask_invalid_model_line = df["model_line"].str.contains(INVALID_BRAND_OR_MODEL, na=False, regex=True)
    model_line_in_brand = [str(m) in str(b) for m, b in zip(df["model_line"], df["product_brand"])]
    for_amd_in_model_line = df["model_line"].str.contains(r"(?i)\s*\(FOR AMD", na=False) # no left parenthesis on purpose
    series_in_model_line = df["model_line"].str.contains(r"(?i)\s*SERIES", na=False)

    df.loc[mask_invalid_brand, "product_brand"] = df.loc[
        mask_invalid_brand, "raw_name"].str.replace(INVALID_BRAND_OR_MODEL, "", regex=True).str.strip().str.extract(MEMORY_BRAND_PATTERN).iloc[:, 0]

    df.loc[mask_invalid_model_line, "model_line"] = None
    df.loc[model_line_in_brand, "model_line"] = None

    df.loc[for_amd_in_model_line, "model_line"] = df.loc[for_amd_in_model_line, "model_line"].str.split(r"(?i)\s*\(FOR AMD", n=1, regex=True).str[0].str.strip()
    df.loc[series_in_model_line, "model_line"] = df.loc[series_in_model_line, "model_line"].str.split(r"(?i)\s*SERIES", n=1, regex=True).str[0].str.strip()

    return df
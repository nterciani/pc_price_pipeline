from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_STORAGE_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.storage.normalize import normalize_storage_fields

@asset(group_name="storage")
def enriched_storage(cleaned_storage: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_storage.copy()

    df["brand"] = df["raw_name"].str.findall(STORAGE_BRAND_PATTERN).str[0]
    df["capacity"] = df["raw_name"].str.extract(STORAGE_CAPACITY_PATTERN)
    df["form_factor"] = df["raw_name"].str.extract(STORAGE_FORM_FACTOR_PATTERN)

    interfaces = df["raw_name"].str.findall(STORAGE_INTERFACE_PATTERN)
    df["interface"] = interfaces.map(lambda x: max(x, key=len) if x else None) # keep longest interface name

    df = normalize_storage_fields(df)

    df["product_family"] = (
        df["brand"] + " " +
        df["capacity"].fillna("") + " " +
        df["form_factor"].fillna("") + " " +
        df["interface"].fillna("") + " " +
        df["storage_type"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    df["product_id"] = df["product_family"].apply(
        lambda x: generate_product_id(x) if isinstance(x, str) and x else None
    )

    df = df[[d["name"] for d in schema]]

    return df

from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_MEMORY_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.memory.normalize import normalize_memory_fields

@asset(group_name="memory")
def enriched_memory(cleaned_memory: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_memory.copy()

    df["brand"] = df["raw_name"].str.findall(MEMORY_BRAND_PATTERN).str[0]
    df["memory_type"] = df["raw_name"].str.extract(MEMORY_TYPE_PATTERN)
    df["speed"] = df["raw_name"].str.extract(MEMORY_SPEED_PATTERN)
    df["capacity"] = df["raw_name"].str.extract(MEMORY_CAPACITY_PATTERN)
    df["modules"] = df["raw_name"].str.extract(MEMORY_MODULES_PATTERN)

    df = normalize_memory_fields(df)

    df["product_family"] = (
        df["brand"] + " " +
        df["memory_type"].fillna("") + " " +
        df["speed"].fillna("") + " " +
        df["capacity"].fillna("") + " " +
        df["modules"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    df["product_id"] = df["product_family"].apply(
        lambda x: generate_product_id(x) if isinstance(x, str) and x else None
    )

    df = df[[d["name"] for d in schema]]

    return df

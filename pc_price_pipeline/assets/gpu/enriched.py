from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_GPUS_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.gpu.normalize import normalize_gpu_fields


@asset(group_name="gpus")
def enriched_gpus(cleaned_gpus: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_gpus.copy()

    df["brand"] = df["raw_name"].str.findall(GPU_BRAND_PATTERN).str[0]
    df["chipset"] = df["raw_name"].str.findall(GPU_CHIPSET_PATTERN).str[0]
    df["memory"] = df["raw_name"].str.extract(GPU_MEMORY_PATTERN)
    df["memory_type"] = df["raw_name"].str.extract(GPU_MEMORY_TYPE_PATTERN)

    df = normalize_gpu_fields(df)

    df["product_family"] = (
        df["brand"] + " " +
        df["chipset"].fillna("") + " " +
        df["memory"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    df["product_id"] = df["product_family"].apply(
        lambda x: generate_product_id(x) if isinstance(x, str) and x else None
    )

    df = df[[d["name"] for d in schema]]

    return df

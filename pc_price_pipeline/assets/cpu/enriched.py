from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_CPUS_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.cpu.normalize import normalize_cpu_fields

@asset(group_name="cpus")
def enriched_cpus(cleaned_cpus: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_cpus.copy()

    df["product_family"] = df["raw_name"].str.extract(CPU_NAME_PATTERN).iloc[:, 0]
    df["brand"] = df["raw_name"].str.extract(CPU_BRAND_PATTERN).iloc[:, 0]
    df["socket"] = df["raw_name"].str.extract(CPU_SOCKET_PATTERN)
    df["product_id"] = df["product_family"].apply(generate_product_id)

    df = normalize_cpu_fields(df)

    df = df[[d["name"] for d in schema]]

    return df

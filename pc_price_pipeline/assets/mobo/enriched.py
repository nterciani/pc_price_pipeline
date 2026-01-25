from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_MOBOS_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.mobo.normalize import normalize_mobo_fields

@asset(group_name="mobos")
def enriched_mobos(cleaned_mobos: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_mobos.copy()

    df["brand"] = df["raw_name"].str.findall(MOBO_BRAND_PATTERN).str[0]
    df["socket"] = df["raw_name"].str.extract(MOBO_SOCKET_PATTERN)
    df["form_factor"] = df["raw_name"].str.extract(MOBO_FORM_FACTOR_PATTERN)
    df["chipset"] = df["raw_name"].str.extract(MOBO_CHIPSET_PATTERN)
    df["memory_type"] = df["raw_name"].str.extract(MOBO_MEMORY_TYPE_PATTERN)
    df["wifi"] = df["raw_name"].str.contains("WiFi|Wi-Fi", case=False)

    df = normalize_mobo_fields(df)

    df["product_family"] = (
        df["brand"] + " " +
        df["chipset"].fillna("") + " " +
        df["socket"].fillna("") + " " +
        df["form_factor"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    df["product_id"] = df["product_family"].apply(
        lambda x: generate_product_id(x) if isinstance(x, str) and x else None
    )

    df = df[[d["name"] for d in schema]]

    return df

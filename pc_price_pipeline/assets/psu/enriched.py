from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import ENRICHED_PSU_SCHEMA as schema
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.psu.normalize import normalize_psu_fields

@asset(group_name="psus")
def enriched_psus(cleaned_psus: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches cleaned data with analytical fields.
    """
    df = cleaned_psus.copy()

    df["brand"] = df["raw_name"].str.findall(PSU_BRAND_PATTERN).str[0]
    df["psu_type"] = df["raw_name"].str.extract(PSU_TYPE_PATTERN)
    df["efficiency_rating"] = df["raw_name"].str.extract(PSU_EFFICIENCY_PATTERN)
    df["wattage"] = df["raw_name"].str.extract(PSU_WATTAGE_PATTERN)
    df["modular"] = df["raw_name"].str.contains(PSU_MODULAR_PATTERN, regex=True)

    df = normalize_psu_fields(df)

    df["product_family"] = (
        df["brand"] + " " +
        df["wattage"].fillna("") + " " +
        df["efficiency_rating"].fillna("") + " " +
        df["psu_type"].fillna("")
    ).str.replace(r"\s+", " ", regex=True).str.strip()

    df["product_id"] = df["product_family"].apply(
        lambda x: generate_product_id(x) if isinstance(x, str) and x else None
    )

    df = df[[d["name"] for d in schema]]

    return df

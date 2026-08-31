import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.storage.normalize import normalize_storage_specs


class StorageTransformer(Transformer):
    def __init__(self, df_raw: pd.DataFrame, brand_pattern: str, specs_schema: list[dict]):
        super().__init__(df_raw, brand_pattern, specs_schema)

    def get_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts the product name from the raw name series.
        Prerequisite: Requires get_specs to be called first to extract the chipset and memory fields.
        """

        df["product_name"] = (
            df["product_brand"] + " " +
            df["model_line"].fillna("") + " " +
            df["capacity"].fillna("") + " " +
            df["form_factor"].fillna("") + " " +
            df["interface"].fillna("") + " " +
            df["storage_type"].fillna("")
        ).str.replace(r"\s+", " ", regex=True).str.strip()

        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["model_line"] = df["raw_name"].str.replace(r"(?i)SSD", " ", regex=True).str.extract(STORAGE_MODEL_LINE_PATTERN).iloc[:, 0]
        df["capacity"] = df["raw_name"].str.extract(STORAGE_CAPACITY_PATTERN)
        df["form_factor"] = df["raw_name"].str.extract(STORAGE_FORM_FACTOR_PATTERN)

        interfaces = df["raw_name"].str.findall(STORAGE_INTERFACE_PATTERN)
        df["interface"] = interfaces.map(lambda x: max(x, key=len) if x else None) # keep longest interface name

        df["storage_type"] = df["raw_name"].str.extract(STORAGE_TYPE_PATTERN)
        df["heatsink"] = df["raw_name"].str.contains("HEATSINK|HEAT SINK", case=False)

        df = normalize_storage_specs(df)
        df["needs_review"] = df[["model_line", "capacity", "form_factor", "interface", "storage_type", "heatsink"]].isnull().any(axis=1)

        return df
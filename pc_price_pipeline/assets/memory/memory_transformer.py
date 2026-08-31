import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.memory.normalize import normalize_memory_specs


class MemoryTransformer(Transformer):
    def __init__(self, df_raw: pd.DataFrame, brand_pattern: str, specs_schema: list[dict]):
        super().__init__(df_raw, brand_pattern, specs_schema)

    def get_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts the product name from the raw name series.
        Prerequisite: Requires get_specs to be called first to extract the chipset and memory fields.
        """

        df["product_name"] = (
            df["product_brand"].fillna("") + " " +
            df["model_line"].fillna("") + " " +
            df["memory_type"].fillna("") + " " +
            df["capacity"].fillna("") + " " +
            df["speed"].fillna("") + " " +
            df["modules"].fillna("") + " " +
            df["cas_latency"].fillna("") + " " +
            df["color"].fillna("")
        ).str.replace(r"\s+", " ", regex=True).str.strip()

        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["model_line"] = df["raw_name"].str.extract(MEMORY_MODEL_LINE_PATTERN).iloc[:, 0]
        df["memory_type"] = df["raw_name"].str.extract(MEMORY_TYPE_PATTERN)
        df["capacity"] = df["raw_name"].str.extract(MEMORY_CAPACITY_PATTERN)
        df["speed"] = df["raw_name"].str.extract(MEMORY_SPEED_PATTERN)
        df["modules"] = df["raw_name"].str.extract(MEMORY_MODULES_PATTERN)
        df["cas_latency"] = df["raw_name"].str.extract(MEMORY_CAS_LATENCY_PATTERN)
        df["color"] = df["source_url"].str.extract(MEMORY_COLOR_PATTERN).iloc[:, 0]

        df = normalize_memory_specs(df)
        df["needs_review"] = df[["model_line", "memory_type", "capacity", "speed", "modules", "cas_latency"]].isnull().any(axis=1)

        return df
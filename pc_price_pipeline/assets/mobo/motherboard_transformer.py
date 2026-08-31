import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.mobo.normalize import normalize_motherboard_specs


class MotherboardTransformer(Transformer):
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
            df["chipset"].fillna("") + " " +
            df["socket"].fillna("") + " " +
            df["form_factor"].fillna("")
        ).str.replace(r"\s+", " ", regex=True).str.strip()

        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["model_line"] = df["raw_name"].str.extract(MOTHERBOARD_MODEL_LINE_PATTERN).iloc[:, 0]
        df["chipset"] = df["raw_name"].str.extract(MOBO_CHIPSET_PATTERN)
        df["socket"] = df["raw_name"].str.extract(MOBO_SOCKET_PATTERN)
        df["form_factor"] = df["raw_name"].str.extract(MOTHERBOARD_FORM_FACTOR_PATTERN)
        df["memory_type"] = df["raw_name"].str.extract(MOBO_MEMORY_TYPE_PATTERN)
        df["wifi"] = df["raw_name"].str.contains("WiFi|Wi-Fi", case=False)

        df = normalize_motherboard_specs(df)
        df["needs_review"] = df[["model_line", "chipset", "socket", "form_factor", "memory_type", "wifi"]].isnull().any(axis=1)

        return df
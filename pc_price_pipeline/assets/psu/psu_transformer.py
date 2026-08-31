import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.psu.normalize import normalize_psu_specs


class PsuTransformer(Transformer):
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
            df["wattage"].fillna("") + " " +
            df["efficiency_rating"].fillna("") + " " +
            df["psu_type"].fillna("") + " " +
            df["color"].fillna("")
        ).str.replace(r"\s+", " ", regex=True).str.strip()

        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["model_line"] = df["raw_name"].str.extract(PSU_MODEL_LINE_PATTERN).iloc[:, 0]
        df["psu_type"] = df["raw_name"].str.extract(PSU_TYPE_PATTERN).iloc[:, 0]
        df["efficiency_rating"] = df["raw_name"].str.extract(PSU_EFFICIENCY_PATTERN)
        df["wattage"] = df["raw_name"].str.extract(PSU_WATTAGE_PATTERN)
        df["modular"] = df["raw_name"].str.contains(PSU_MODULAR_PATTERN, regex=True)
        df["color"] = df["source_url"].str.extract(PSU_COLOR_PATTERN).iloc[:, 0]

        df = normalize_psu_specs(df)
        df["needs_review"] = df[["model_line", "psu_type", "efficiency_rating", "wattage", "modular", "color"]].isnull().any(axis=1)

        return df
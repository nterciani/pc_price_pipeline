import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.gpu.normalize import normalize_gpu_specs


class GpuTransformer(Transformer):
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
            df["chipset"].fillna("") + " " +
            df["memory"].fillna("")
        ).str.replace(r"\s+", " ", regex=True).str.strip()

        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["chipset"] = df["raw_name"].str.findall(GPU_CHIPSET_PATTERN).str[0]
        df["memory"] = df["raw_name"].str.extract(GPU_MEMORY_PATTERN)
        df["memory_type"] = df["raw_name"].str.extract(GPU_MEMORY_TYPE_PATTERN)
        df["model_line"] = df["raw_name"].str.extract(GPU_MODEL_LINE_PATTERN).iloc[:, 0]
        df["overclocked"] = df["raw_name"].str.contains(GPU_OVERCLOCKED_PATTERN, case=False, na=False)

        df = normalize_gpu_specs(df)
        df["needs_review"] = df[["chipset", "memory", "memory_type", "model_line"]].isnull().any(axis=1)

        return df
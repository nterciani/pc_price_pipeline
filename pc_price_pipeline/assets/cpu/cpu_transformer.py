import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.cpu.normalize import normalize_cpu_specs


class CpuTransformer(Transformer):
    def __init__(self, df_raw: pd.DataFrame, brand_pattern: str, specs_schema: list[dict]):
        super().__init__(df_raw, brand_pattern, specs_schema)

    def get_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product name from the raw name series."""
        df["product_name"] = df["raw_name"].str.extract(CPU_NAME_PATTERN).iloc[:, 0].str.upper()
        return df

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts the product's specs from the current dataframe and adds them as new columns."""

        df["socket"] = df["raw_name"].str.extract(CPU_SOCKET_PATTERN)
        df["core_count"] = df["raw_name"].str.extract(CPU_CORES_PATTERN)
        df["core_clock"] = df["raw_name"].str.extract(CPU_CLOCK_SPEED_PATTERN)
        df["thread_count"] = df["raw_name"].str.extract(CPU_THREADS_PATTERN)
        df["integrated_graphics"] = df["raw_name"].str.extract(CPU_INTEGRATED_GRAPHICS_PATTERN).iloc[:, 0]
        df["tdp"] = df["raw_name"].str.extract(CPU_TDP_PATTERN)

        df = normalize_cpu_specs(df)
        df["needs_review"] = df[["socket", "core_count", "core_clock", "thread_count", "integrated_graphics", "tdp"]].isnull().any(axis=1)

        return df
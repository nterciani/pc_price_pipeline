import pandas as pd
from pc_price_pipeline.assets.common.utils import *

MEMORY_MAP = {
    r"(\d+)\s*G$": r"\1GB",
    r"(\d+) GB": r"\1GB",
}

CHIPSET_MAP = {
    r"(RTX|GTX|GT)(\d+)": r"\1 \2",
    r"AMD RX (\d+) (XT|XTX|GRE)?": r"RADEON RX \1 \2",
    r"^RX (\d+) (XT|XTX|GRE)?$": r"RADEON RX \1 \2",
}

GPU_MODEL_LINE_SUFFIX = r"(?i)\s+\b(?:NVIDIA|RADEON|GEFORCE|RTX|GTX|G[- ]?SYNC|SUPPORT)\b.*$"


def normalize_gpu_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)

    df["chipset"] = df["chipset"].apply(normalize_text)
    df["chipset"] = df["chipset"].replace(CHIPSET_MAP, regex=True)

    df["memory"] = df["memory"].apply(normalize_text)
    df["memory"] = df["memory"].replace(MEMORY_MAP, regex=True)

    # get rid of unrealistic memory values
    df['mem_val'] = df['memory'].str.extract(r'(\d+)').astype(float)
    df = df[df['mem_val'] < 512]
    df = df.drop(columns=['mem_val'])

    df["model_line"] = df["model_line"].apply(normalize_text)
    mask_nvidia_founder = df["raw_name"].str.contains(r"(?i)Founders Edition", na=False)

    df["model_line"] = df["model_line"].str.replace(GPU_MODEL_LINE_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(
        r"(?i)\s+OC\s+(?:EDITION|VERSION)\b.*$", " OC", regex=True
    )
    df["model_line"] = df["model_line"].str.replace(r"\s+", " ", regex=True).str.strip()
    df["model_line"] = df["model_line"].replace(r"^$", None, regex=True)
    df.loc[df["model_line"].str.len().ge(30), "model_line"] = None
    df.loc[mask_nvidia_founder, "model_line"] = "FOUNDERS EDITION"

    df["memory_type"] = df["memory_type"].apply(normalize_text)

    return df

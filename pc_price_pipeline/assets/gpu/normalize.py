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

def normalize_gpu_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)

    df["chipset"] = df["chipset"].apply(normalize_text)
    df["chipset"] = df["chipset"].replace(CHIPSET_MAP, regex=True)

    df["memory"] = df["memory"].apply(normalize_text)
    df["memory"] = df["memory"].replace(MEMORY_MAP, regex=True)

    # get rid of unrealistic memory values
    df['mem_val'] = df['memory'].str.extract(r'(\d+)').astype(float)
    df = df[df['mem_val'] < 512]
    df = df.drop(columns=['mem_val'])

    df["memory_type"] = df["memory_type"].apply(normalize_text)

    return df

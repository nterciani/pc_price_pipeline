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

    # get rid of unrealistic model-line values
    df['model_line'] = df['model_line'].apply(normalize_text)

    mask = df["model_line"].str.len() >= 30
    df.loc[mask, "model_line"] = None

    mask_brand = [str(b) in str(m) for b, m in zip(df["product_brand"], df["model_line"])]
    mask_nvidia_founder = df["raw_name"].str.contains(r"(?i)Founders Edition")
    oc_mask = df["model_line"].str.endswith("OC", na=False)
    
    df.loc[oc_mask, "model_line"] = df.loc[oc_mask, "model_line"].str.replace(r"(?i)\s*OC$", "", regex=True)

    df.loc[mask_brand, "model_line"] = [
        model.strip(brand) 
        for model, brand in zip(
            df.loc[mask_brand, "model_line"].astype(str), 
            df.loc[mask_brand, "product_brand"].astype(str)
        )
    ]

    df["model_line"] = df["model_line"].replace(r"NVIDIA|RADEON", "", regex=True)
    df["model_line"] = df["model_line"].replace(r"^\s*$", None, regex=True)
    df.loc[mask_nvidia_founder, "model_line"] = "FOUNDERS EDITION"

    df["memory_type"] = df["memory_type"].apply(normalize_text)

    return df
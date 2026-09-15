import pandas as pd
from pc_price_pipeline.assets.common.utils import *

BRAND_MAP = {
    r"WD (?:BLUE|BLACK|RED|PURPLE|GOLD|GREEN) ?(?:PRO|PLUS)?": "WESTERN DIGITAL",
    r"WD WD\w+": "WESTERN DIGITAL",
}

INTERFACE_MAP = {
    r"PCI EXPRESS (?:NVME )?(\d\.0) (X\d)": r"PCIE \1 \2",
    r"PCI EXPRESS (?:NVME )?(\d\.0)": r"PCIE \1",
    r"PCIE GEN ?(\d)(?:\.0)? ?(X\d)": r"PCIE \1.0 \2",
    r"PCIE GEN ?(\d)(?:\.0)?(?: NVME)": r"PCIE \1.0",
    r"PCIE® (\d\.0) ?(X\d)": r"PCIE \1 \2",
    r"(?:PCIE )?GEN(\d)(?: NVME| PCIE)?": r"PCIE \1.0",
    r"PCIE (\d\.0) NVME": r"PCIE \1",
    r"PCIE NVME": r"PCIE",
    r"PCIE (\d\.0)(X\d)": r"PCIE \1 \2",
}

FORM_FACTOR_MAP = {
    r"(\d\.\d) ?\w+": r'\1"',
    r"(\d\.\d)”": r'\1"',
}

STORAGE_TYPE_MAP = {
    r"(?i)(?:SOLID STATE DRIVE|SSD)": "SSD",
    r"(?i)(?:HARD DISK DRIVE|HARD DRIVE|HDD)": "HDD",
}

MODEL_MAP = {
    r"W HEATSINK": "WITH HEATSINK",
    r"\S*-\S*": "",
    r"\d+G(?:B)?|\d+MB|\d+TB": "",
    r"®|™|©": "",
    r"SERIES": "",
    r"WD\w+": "",
    r"WD ": "",
    r"HD\w+": "",
    r"MG\w{4,}": "",
    r"ST\w+": "",
}

STORAGE_MODEL_LINE_SUFFIX = r"(?i)\s+\b(?:\d+(?:\.\d+)?\s*(?:MB|GB|TB)|SSD|HDD|SOLID\s+STATE\s+DRIVE|HARD\s+(?:DISK\s+)?DRIVE|M\.2(?:\s+\d{2,4})?|NVME|NMVE|GEN\s*\d+(?:\.\d+)?|SATA|PCI(?:E|-?\s*EXPRESS)|INTERNAL|WITH\s+HEATSINK|HEATSINK|SERIES|\d{4}\s+RPM(?:\s+SAS)?)\b.*$"


def normalize_storage_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)
    df["product_brand"] = df["product_brand"].replace(BRAND_MAP, regex=True)

    products_to_drop = df["product_brand"].str.contains(r"\d+(?:MG|GB|TB)?", na=False)
    df = df[~products_to_drop].copy()

    df["capacity"] = df["capacity"].apply(normalize_text)

    df["model_line"] = df["model_line"].apply(normalize_text)
    df["model_line"] = df["model_line"].str.replace(STORAGE_MODEL_LINE_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].replace(MODEL_MAP, regex=True).str.strip()
    df["model_line"] = df["model_line"].str.replace(r"\s+", " ", regex=True).str.strip()

    df["form_factor"] = df["form_factor"].apply(normalize_text)
    df["form_factor"] = df["form_factor"].astype(str).replace(FORM_FACTOR_MAP, regex=True)

    df["interface"] = df["interface"].apply(normalize_text)
    df["interface"] = df["interface"].replace(INTERFACE_MAP, regex=True)

    df["storage_type"] = df["storage_type"].apply(normalize_text)
    df["storage_type"] = df["storage_type"].replace(STORAGE_TYPE_MAP, regex=True)

    return df

import pandas as pd
from pc_price_pipeline.assets.common.utils import *

INTERFACE_MAP = {
    r"PCI EXPRESS (?:NVME )?(\d\.0) (X\d)": r"PCIE \1 \2",
    r"PCI EXPRESS (?:NVME )?(\d\.0)": r"PCIE \1",
    r"PCIE GEN ?(\d)(?:\.0)? ?(X\d)": r"PCIE \1.0 \2",
    r"PCIE GEN ?(\d)(?:\.0)?(?: NVME)": r"PCIE \1.0",
    r"PCIE® (\d\.0) ?(X\d)": r"PCIE \1 \2",
    r"(?:PCIE )?GEN(\d)(?: NVME| PCIE)?": r"PCIE \1.0",
    r"PCIE (\d\.0) NVME": r"PCIE \1",
    r"PCIE NVME": r"PCIE"
}

FORM_FACTOR_MAP = {
    r"(\d\.\d) ?\w+": r'\1"',
    r"(\d\.\d)”": r'\1"',
}

def normalize_storage_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)
    df["capacity"] = df["capacity"].apply(normalize_text).str.replace(' ', '')

    df["form_factor"] = df["form_factor"].apply(normalize_text)
    df["form_factor"] = df["form_factor"].replace(FORM_FACTOR_MAP, regex=True)

    df["interface"] = df["interface"].apply(normalize_text)
    df["interface"] = df["interface"].replace(INTERFACE_MAP, regex=True)

    return df

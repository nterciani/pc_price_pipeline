import pandas as pd
from pc_price_pipeline.assets.common.utils import *

WATTAGE_MAP = {
    r"(?:[A-Z\-\s]+)?(\d+)(?:[A-Z\s]+)?": r"\1W"
}

EFFICIENCY_MAP = {
    r"CYBENETICS ?(BRONZE|SILVER|GOLD|PLATINUM|TITANIUM)": r"CYBENETICS \1",
    r"(?i)^(?!CYBENETICS)(?:80)? ?(?:PLUS®?|\+)? ?(BRONZE|SILVER|GOLD|PLATINUM|TITANIUM)": r"80+ \1",
    r"80 PLUS": r"80+",
}

def normalize_psu_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["brand"] = df["brand"].apply(normalize_text)
    df["psu_type"] = df["psu_type"].apply(normalize_text).str.replace("SFX L", "SFX-L")

    df["efficiency_rating"] = df["efficiency_rating"].apply(normalize_text)
    df["efficiency_rating"] = df["efficiency_rating"].replace(EFFICIENCY_MAP, regex=True).str.replace(" CERTIFIED", "")

    df["wattage"] = df["wattage"].apply(normalize_text).str.replace(" ", "")
    df["wattage"] = df["wattage"].replace(WATTAGE_MAP, regex=True)

    return df

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

PSU_MODEL_LINE_SUFFIX = r"(?i)\s+\b(?:ATX(?:\s*3(?:\.\s*1)?)?|SFX(?:-?L)?|TFX|\d{3,4}\s*W(?:ATT)?|80\s*(?:PLUS|\+)\s+(?:BRONZE|SILVER|GOLD|PLATINUM|TITANIUM)|CYBENETICS\s+\w+|FULLY\s+MODULAR|MODULAR|FRENCH\s+VERSION)\b.*$"
PSU_REVISION_SUFFIX = r"\s*\(\d{4}\)\s*$"
PSU_GENERIC_MODEL_LINE = r"(?i)\b(?:IS\s+A\s+POWER\s+SUPPLY|POWER\s+SUPPLY\s+WITH)\b"


def normalize_psu_specs(df: pd.DataFrame) -> pd.DataFrame:
    df["product_brand"] = df["product_brand"].apply(normalize_text)

    # backfall null psu types onto link
    df["psu_type"] = df["psu_type"].fillna(df["source_url"].str.extract(PSU_TYPE_PATTERN).iloc[:, 0])

    df["psu_type"] = df["psu_type"].apply(normalize_text).str.replace("SFX L", "SFX-L")

    df["model_line"] = df["model_line"].apply(normalize_text)
    df["model_line"] = df["model_line"].str.replace(PSU_GENERIC_MODEL_LINE, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(r"(?i)\bPOWER\s+SUPPLY\b", "", regex=True)
    df["model_line"] = df["model_line"].str.replace(PSU_REVISION_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(PSU_MODEL_LINE_SUFFIX, "", regex=True)
    df["model_line"] = df["model_line"].str.replace(r"\s+", " ", regex=True).str.strip()

    df["efficiency_rating"] = df["efficiency_rating"].apply(normalize_text)
    df["efficiency_rating"] = df["efficiency_rating"].replace(EFFICIENCY_MAP, regex=True).str.replace(" CERTIFIED", "")

    df["wattage"] = df["wattage"].apply(normalize_text).str.replace(" ", "")
    df["wattage"] = df["wattage"].replace(WATTAGE_MAP, regex=True)

    return df

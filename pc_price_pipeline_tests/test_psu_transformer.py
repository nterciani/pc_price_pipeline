import pytest

from pc_price_pipeline.assets.common.star_schemas import DIM_PSU_SPECS
from pc_price_pipeline.assets.common.utils import PSU_BRAND_PATTERN
from pc_price_pipeline.assets.psu.psu_transformer import PsuTransformer


@pytest.mark.parametrize(
    ("raw_name", "expected_model_line"),
    [
        ("Corsair HX1200I (2025) 1200W ATX Power Supply 80 Plus Titanium Efficiency", "HX1200I"),
        ("AZZA PSAZ-550W French Version 550 W Intel ATX12V 80 PLUS BRONZE Certified Non-Modular Power Supply", "PSAZ"),
        ("Thermaltake Toughpower GF A3 Snow Edition 1050W 80+ Gold Full Modular SLI/Crossfire Ready ATX 3.0 Power Supply;", "TOUGHPOWER GF A3 SNOW EDITION"),
    ],
)
def test_psu_model_line_removes_metadata_suffixes(raw_listing, raw_name, expected_model_line):
    raw = raw_listing(raw_name, "PSU")

    result = PsuTransformer(raw, PSU_BRAND_PATTERN, DIM_PSU_SPECS).clean_to_intermediate(raw)

    row = result.iloc[0]
    assert row["model_line"] == expected_model_line
    assert "FRENCH" not in row["model_line"]
    assert "POWER SUPPLY" not in row["model_line"]
    assert "(" not in row["model_line"]


def test_psu_type_can_fall_back_to_source_url(raw_listing):
    raw = raw_listing(
        "ASRock TC-1650T 1650 W PCIe5.1 Cybenetics Titanium Full Modular Power Supply",
        "PSU",
        "https://www.example.com/asrock-atx3-1-pcie5-1-1650-w-cybenetics-titanium-power-supply-black-tc-1650t",
    )

    result = PsuTransformer(raw, PSU_BRAND_PATTERN, DIM_PSU_SPECS).clean_to_intermediate(raw)

    assert result.iloc[0]["psu_type"] == "ATX"

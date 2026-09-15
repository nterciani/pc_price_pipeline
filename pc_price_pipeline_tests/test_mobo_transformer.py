import pytest

from pc_price_pipeline.assets.common.star_schemas import DIM_MOTHERBOARD_SPECS
from pc_price_pipeline.assets.common.utils import MOTHERBOARD_BRAND_PATTERN
from pc_price_pipeline.assets.motherboard.motherboard_transformer import MotherboardTransformer


@pytest.mark.parametrize(
    ("raw_name", "expected_model_line"),
    [
        ("MSI MAG B550 TOMAHAWK MAX WIFI, AMD B550 ATX AM4 DDR4", "MAG B550 TOMAHAWK MAX WIFI"),
        ("ASUS B650E MAX GAMING WIFI - AM5 ATX DDR5", "B650E MAX GAMING WIFI"),
        ("ASUS B650M C V3 (REV. 1.0) AM5 Micro-ATX DDR5", "B650M C V3"),
    ],
)
def test_motherboard_model_line_removes_metadata_suffixes(raw_listing, raw_name, expected_model_line):
    raw = raw_listing(raw_name, "Motherboard")

    result = MotherboardTransformer(
        raw, MOTHERBOARD_BRAND_PATTERN, DIM_MOTHERBOARD_SPECS
    ).clean_to_intermediate(raw)

    row = result.iloc[0]
    assert row["model_line"] == expected_model_line
    assert not row["model_line"].endswith((",", "-"))
    assert "REV." not in row["model_line"]
    assert "DDR" not in row["model_line"]


def test_motherboard_model_line_preserves_meaningful_gaming(raw_listing):
    raw = raw_listing("ASUS PRO WS W880-ACE SE GAMING DESKTOP LGA 1700 ATX", "Motherboard")

    result = MotherboardTransformer(
        raw, MOTHERBOARD_BRAND_PATTERN, DIM_MOTHERBOARD_SPECS
    ).clean_to_intermediate(raw)

    assert "GAMING" in result.iloc[0]["model_line"]

import pytest

from pc_price_pipeline.assets.common.star_schemas import DIM_STORAGE_SPECS
from pc_price_pipeline.assets.common.utils import STORAGE_BRAND_PATTERN
from pc_price_pipeline.assets.storage.storage_transformer import StorageTransformer


@pytest.mark.parametrize(
    ("raw_name", "expected_model_line"),
    [
        ("Seagate EXOS X18 7200 RPM SAS 18TB 3.5 Inch HDD", "EXOS X18"),
        ("Crucial T700 GEN5 NMVE 2TB M.2 PCIe 5.0 SSD", "T700"),
    ],
)
def test_storage_model_line_stops_at_product_model(raw_listing, raw_name, expected_model_line):
    raw = raw_listing(raw_name, "Storage")

    result = StorageTransformer(raw, STORAGE_BRAND_PATTERN, DIM_STORAGE_SPECS).clean_to_intermediate(raw)

    assert result.iloc[0]["model_line"] == expected_model_line


@pytest.mark.parametrize(
    "raw_name",
    [
        "22 165 885 2TB",
        "801888 B21 1TB 2.5 Inch HDD",
    ],
)
def test_storage_legacy_codes_are_flagged_or_retained_without_empty_models(raw_listing, raw_name):
    raw = raw_listing(raw_name, "Storage")

    result = StorageTransformer(raw, STORAGE_BRAND_PATTERN, DIM_STORAGE_SPECS).clean_to_intermediate(raw)

    assert len(result) <= 1
    if not result.empty:
        assert result.iloc[0]["model_line"] or bool(result.iloc[0]["needs_review"])

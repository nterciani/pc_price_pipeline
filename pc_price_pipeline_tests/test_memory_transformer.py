from pc_price_pipeline.assets.common.star_schemas import DIM_MEMORY_SPECS
from pc_price_pipeline.assets.common.utils import MEMORY_BRAND_PATTERN
from pc_price_pipeline.assets.memory.memory_transformer import MemoryTransformer


def test_memory_transformer_extracts_specs_and_product_key(raw_listing):
    raw = raw_listing(
        "CORSAIR Vengeance RGB 32GB 2 x 16GB DDR5 6000 Desktop Memory",
        "Memory",
    )

    result = MemoryTransformer(raw, MEMORY_BRAND_PATTERN, DIM_MEMORY_SPECS).clean_to_intermediate(raw)

    row = result.iloc[0]
    assert row["product_brand"] == "CORSAIR"
    assert row["memory_type"] == "DDR5"
    assert row["capacity"] == "32GB"
    assert isinstance(row["product_key"], str)

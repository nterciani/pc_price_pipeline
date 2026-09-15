from pc_price_pipeline.assets.common.star_schemas import DIM_CPU_SPECS
from pc_price_pipeline.assets.common.utils import CPU_BRAND_PATTERN
from pc_price_pipeline.assets.cpu.cpu_transformer import CpuTransformer


def test_cpu_transformer_extracts_current_intermediate_contract(raw_listing):
    raw = raw_listing(
        "AMD Ryzen 7 5800X 8-Core 3.8 GHz Socket AM4 105W Processor",
        "CPU",
    )

    result = CpuTransformer(raw, CPU_BRAND_PATTERN, DIM_CPU_SPECS).clean_to_intermediate(raw)

    row = result.iloc[0]
    assert row["product_brand"] == "AMD"
    assert row["product_name"] == "AMD RYZEN 7 5800X"
    assert row["socket"] == "AM4"
    assert isinstance(row["product_key"], str)


def test_cpu_transformer_marks_incomplete_specs_for_review(raw_listing):
    raw = raw_listing("AMD Ryzen 7 5800X", "CPU")

    result = CpuTransformer(raw, CPU_BRAND_PATTERN, DIM_CPU_SPECS).clean_to_intermediate(raw)

    assert bool(result.iloc[0]["needs_review"])

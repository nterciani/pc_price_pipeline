import pytest

from pc_price_pipeline.assets.common.star_schemas import DIM_GPU_SPECS
from pc_price_pipeline.assets.common.utils import GPU_BRAND_PATTERN
from pc_price_pipeline.assets.gpu.gpu_transformer import GpuTransformer


@pytest.mark.parametrize(
    ("raw_name", "expected_model_line"),
    [
        ("MSI N750TI 2GD5 OC G SYNC SUPPORT GeForce GTX 750 Ti 2GB", "N750TI 2GD5 OC"),
        ("MSI TWIN EDGE OC RTX 3050 6GB GeForce RTX 3050 6GB", "TWIN EDGE OC"),
        ("ASUS DUAL OC RTX 5070 GeForce RTX 5070 12GB", "DUAL OC"),
    ],
)
def test_gpu_model_line_excludes_chipset_and_memory(raw_listing, raw_name, expected_model_line):
    raw = raw_listing(raw_name, "GPU")

    result = GpuTransformer(raw, GPU_BRAND_PATTERN, DIM_GPU_SPECS).clean_to_intermediate(raw)

    row = result.iloc[0]
    assert row["model_line"] == expected_model_line
    assert row["chipset"]
    assert row["memory"]
    assert "RTX" not in row["model_line"]
    assert "GB" not in row["model_line"]

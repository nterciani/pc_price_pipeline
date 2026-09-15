from unittest.mock import patch

from pc_price_pipeline.assets.common.star_schemas import (
    DIM_CPU_SPECS,
    FACT_VECTOR_SEARCH_SCHEMA,
)
from pc_price_pipeline.assets.common.cleaned_prices import cleaned_prices_df
from pc_price_pipeline.assets.common.transformer import Transformer
from pc_price_pipeline.assets.common.utils import CPU_BRAND_PATTERN
from pc_price_pipeline.assets.cpu.cpu_transformer import CpuTransformer


def test_base_transformer_hooks_are_explicit(raw_listing):
    transformer = Transformer(raw_listing("example", "CPU"), "pattern", [])

    try:
        transformer.get_name(transformer.df_clean)
    except NotImplementedError:
        pass
    else:
        raise AssertionError("get_name must be implemented by category transformers")


def test_intermediate_to_star_returns_four_frames_without_external_models(raw_listing):
    raw = raw_listing(
        "AMD Ryzen 7 5800X 8-Core 3.8 GHz Socket AM4 105W Processor",
        "CPU",
    )
    transformer = CpuTransformer(raw, CPU_BRAND_PATTERN, DIM_CPU_SPECS)
    cleaned = cleaned_prices_df(raw)
    intermediate = transformer.clean_to_intermediate(cleaned)
    intermediate["product_embedding"] = [[0.1, 0.2]]
    intermediate["match_confidence"] = 1.0
    intermediate["match_method"] = "exact"
    intermediate["is_approved"] = True

    with patch(
        "pc_price_pipeline.assets.common.transformer.generate_product_embeddings",
        side_effect=lambda frame: frame,
    ), patch(
        "pc_price_pipeline.assets.common.transformer.match_intermediate_to_existing_products",
        side_effect=lambda frame: frame,
    ):
        outputs = transformer.intermediate_to_star(intermediate)

    assert len(outputs) == 4
    dim_products, dim_specs, fact_prices, fact_vector_search = outputs
    assert "product_key" in dim_products.columns
    assert "product_key" in dim_specs.columns
    assert "price" in fact_prices.columns
    assert [column["name"] for column in FACT_VECTOR_SEARCH_SCHEMA] == list(fact_vector_search.columns)

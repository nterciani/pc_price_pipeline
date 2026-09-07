import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import GPU_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_GPU_SPECS
from pc_price_pipeline.assets.gpu.gpu_transformer import GpuTransformer


@asset(group_name="gpus")
def transformed_gpus(cleaned_gpus: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms cleaned GPU data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_gpu_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = GpuTransformer(cleaned_gpus, GPU_BRAND_PATTERN, DIM_GPU_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_clean)

    return transformer.intermediate_to_star(df_intermediate)

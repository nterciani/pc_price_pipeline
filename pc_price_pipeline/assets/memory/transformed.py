import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import MEMORY_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_MEMORY_SPECS
from pc_price_pipeline.assets.memory.memory_transformer import MemoryTransformer



@asset(group_name="memory")
def transformed_memory(cleaned_memory: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms cleaned memory data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_memory_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = MemoryTransformer(cleaned_memory, MEMORY_BRAND_PATTERN, DIM_MEMORY_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_clean)

    return transformer.intermediate_to_star(df_intermediate)

import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import STORAGE_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_STORAGE_SPECS
from pc_price_pipeline.assets.storage.storage_transformer import StorageTransformer


@asset(group_name="storage")
def transformed_storage(cleaned_storage: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms cleaned storage data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_storage_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = StorageTransformer(cleaned_storage, STORAGE_BRAND_PATTERN, DIM_STORAGE_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_clean)

    return transformer.intermediate_to_star(df_intermediate)

import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import PSU_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_PSU_SPECS
from pc_price_pipeline.assets.psu.psu_transformer import PsuTransformer


@asset(group_name="psus")
def transformed_psus(cleaned_psus: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms cleaned psu data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_psu_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = PsuTransformer(cleaned_psus, PSU_BRAND_PATTERN, DIM_PSU_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_clean)

    return transformer.intermediate_to_star(df_intermediate)

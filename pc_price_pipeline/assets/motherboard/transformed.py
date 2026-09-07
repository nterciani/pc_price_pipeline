import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import MOTHERBOARD_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_MOTHERBOARD_SPECS
from pc_price_pipeline.assets.motherboard.motherboard_transformer import MotherboardTransformer


@asset(group_name="motherboards")
def transformed_motherboards(cleaned_motherboards: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms cleaned motherboard data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_motherboard_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = MotherboardTransformer(cleaned_motherboards, MOTHERBOARD_BRAND_PATTERN, DIM_MOTHERBOARD_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_clean)

    return transformer.intermediate_to_star(df_intermediate)

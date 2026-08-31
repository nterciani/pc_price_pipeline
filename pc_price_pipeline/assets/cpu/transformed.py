import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.utils import CPU_BRAND_PATTERN
from pc_price_pipeline.assets.common.star_schemas import DIM_CPU_SPECS
from pc_price_pipeline.assets.cpu.cpu_transformer import CpuTransformer

@asset(group_name="cpus")
def transformed_cpus(cleaned_cpus: pd.DataFrame) -> tuple[pd.DataFrame]:
    """ Transforms cleaned CPU data into a format suitable for the star schema.
    Returns a tuple of dataframes corresponding to the dim_products, dim_cpu_specs, 
    fact_prices, and fact_vector_search tables in the star schema.
    """
    transformer = CpuTransformer(cleaned_cpus, CPU_BRAND_PATTERN, DIM_CPU_SPECS)

    df_intermediate = transformer.clean_to_intermediate(transformer.df_raw)

    return transformer.intermediate_to_star(df_intermediate)

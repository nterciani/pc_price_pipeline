import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.star_schemas import *
from pc_price_pipeline.assets.common.bigquery_helpers import write_all_to_bq

@asset(group_name="cpus")
def store_cpus(transformed_cpus: tuple[pd.DataFrame]):
    write_all_to_bq(transformed_cpus, "cpu", DIM_CPU_SPECS)

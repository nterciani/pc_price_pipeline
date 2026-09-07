import pandas as pd
from dagster import asset
from pc_price_pipeline.assets.common.star_schemas import *
from pc_price_pipeline.assets.common.bigquery_helpers import write_all_to_bq


@asset(group_name="cpus")
def store_cpus(transformed_cpus: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    write_all_to_bq(transformed_cpus, "cpu", DIM_CPU_SPECS)


@asset(group_name="gpus")
def store_gpus(transformed_gpus: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    write_all_to_bq(transformed_gpus, "gpu", DIM_GPU_SPECS)


@asset(group_name="memory")
def store_memory(transformed_memory: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]) -> None:
    write_all_to_bq(transformed_memory, "memory", DIM_MEMORY_SPECS)
from dagster import asset
import pandas as pd
from pc_price_pipeline.assets.common.schemas import *
from pc_price_pipeline.assets.common.bigquery_write import write_to_bq

@asset(group_name="cpus")
def store_cpus(enriched_cpus: pd.DataFrame):
    write_to_bq(
        enriched_cpus,
        "pc_part_prices.enriched_cpus",
        ENRICHED_CPUS_SCHEMA
    )

@asset(group_name="gpus")
def store_gpus(enriched_gpus: pd.DataFrame):
    write_to_bq(
        enriched_gpus,
        "pc_part_prices.enriched_gpus",
        ENRICHED_GPUS_SCHEMA
    )

@asset(group_name="mobos")
def store_mobos(enriched_mobos: pd.DataFrame):
    write_to_bq(
        enriched_mobos,
        "pc_part_prices.enriched_mobos",
        ENRICHED_MOBOS_SCHEMA
    )

@asset(group_name="memory")
def store_memory(enriched_memory: pd.DataFrame):
    write_to_bq(
        enriched_memory,
        "pc_part_prices.enriched_memory",
        ENRICHED_MEMORY_SCHEMA
    )

@asset(group_name="storage")
def store_storage(enriched_storage: pd.DataFrame):
    write_to_bq(
        enriched_storage,
        "pc_part_prices.enriched_storage",
        ENRICHED_STORAGE_SCHEMA
    )

@asset(group_name="psus")
def store_psus(enriched_psus: pd.DataFrame):
    write_to_bq(
        enriched_psus,
        "pc_part_prices.enriched_psus",
        ENRICHED_PSU_SCHEMA
    )

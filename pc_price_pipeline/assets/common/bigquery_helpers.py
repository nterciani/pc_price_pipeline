import os
import uuid
import google.auth
import pandas as pd
from google.cloud import bigquery
from pandas_gbq import to_gbq, read_gbq
from google.api_core.exceptions import NotFound
from pc_price_pipeline.assets.common.star_schemas import *

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "pc-price-pipeline")
CREDENTIALS, _ = google.auth.default()


def get_staging_table_name(table_name: str) -> str:
    """Return a staging name unique to this process and invocation."""
    return f"{table_name}_{os.getpid()}_{uuid.uuid4().hex}"


def read_from_gbq_data_set(query: str) -> pd.DataFrame:
    if PROJECT_ID is None:
        raise ValueError("GCP_PROJECT_ID environment variable is not set.")

    return read_gbq(query, project_id=PROJECT_ID, credentials=CREDENTIALS)


def write_df_to_staging_bq(df: pd.DataFrame, schema: list[dict], staging_table_name: str):
    table = f"pc_part_prices_star.staging_{staging_table_name}"

    if df.empty:
        raise ValueError(f"{table} is empty — aborting BigQuery write")

    to_gbq(
        df,
        destination_table=table,
        project_id=PROJECT_ID,
        table_schema=schema,
        if_exists="replace",
        credentials=CREDENTIALS,
    )


def ensure_table_exists(table_id: str, schema: list[dict]):
    client = bigquery.Client()
    try:
        client.get_table(table_id)
    except NotFound:
        table = bigquery.Table(f"{client.project}.{table_id}")
        table.schema = schema
        client.create_table(table)



def merge_staging_to_star_table(table: str, schema: list[dict], staging_table_name: str):
    client = bigquery.Client()

    cols = [col["name"] for col in schema]

    update_clause = ", ".join(f"target.{col} = source.{col}" for col in cols)
    insert_cols = ", ".join(cols)
    insert_vals = ", ".join(f"source.{col}" for col in cols)
    order_clause = " + ".join(f"(CASE WHEN {col} IS NOT NULL THEN 1 ELSE 0 END)" for col in cols)

    if "fact_vector_search" in table:
        on_clause = """
            target.product_key = source.product_key
            AND target.raw_name = source.raw_name
            AND target.scraped_at = source.scraped_at
        """
    elif "fact_prices" in table:
        on_clause = """
            target.product_key = source.product_key
            AND target.retailer_key = source.retailer_key
            AND target.price_date = source.price_date
            AND target.source_url = source.source_url
        """
    elif "raw_prices" in table:
        on_clause = """
            target.raw_name = source.raw_name
            AND target.scraped_at = source.scraped_at
            AND target.source_url = source.source_url
        """
    else:
        on_clause = "target.product_key = source.product_key"

    dim_query = f"""
        MERGE `{table}` AS Target
        USING (
            SELECT * EXCEPT(dedup_rank) FROM (
                SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY product_key
                        ORDER BY ({order_clause}) DESC
                ) AS dedup_rank
                FROM `pc_part_prices_star.staging_{staging_table_name}`
            ) WHERE dedup_rank = 1
        ) AS Source
        ON {on_clause}
        WHEN MATCHED THEN UPDATE SET {update_clause}
        WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals});
    """

    raw_query = f"""
        MERGE `{table}` AS Target
        USING (
            SELECT * EXCEPT(dedup_rank) FROM (
                SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY raw_name, scraped_at, source_url
                        ORDER BY ({order_clause}) DESC
                ) AS dedup_rank
                FROM `pc_part_prices_star.staging_{staging_table_name}`
            ) WHERE dedup_rank = 1
        ) AS Source
        ON {on_clause}
        WHEN MATCHED THEN UPDATE SET {update_clause}
        WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals});
    """

    fact_query = f"""
        MERGE `{table}` AS Target
        USING (
            SELECT * EXCEPT(dedup_rank) FROM (
                SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY product_key, retailer_key, price_date, source_url
                        ORDER BY ({order_clause}) DESC
                ) AS dedup_rank
                FROM `pc_part_prices_star.staging_{staging_table_name}`
            ) WHERE dedup_rank = 1
        ) AS Source
        ON {on_clause}
        WHEN MATCHED THEN UPDATE SET {update_clause}
        WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals});
    """

    vector_query = f"""
        MERGE `{table}` AS Target
        USING (
            SELECT * EXCEPT(dedup_rank) FROM (
                SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY product_key, raw_name, scraped_at
                        ORDER BY ({order_clause}) DESC
                ) AS dedup_rank
                FROM `pc_part_prices_star.staging_{staging_table_name}`
            ) WHERE dedup_rank = 1
        ) AS Source
        ON {on_clause}
        WHEN MATCHED THEN UPDATE SET {update_clause}
        WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals});
    """

    if "fact_prices" in table:
        merge_query = fact_query
    elif "fact_vector_search" in table:
        merge_query = vector_query
    elif "raw_prices" in table:
        merge_query = raw_query
    else:
        merge_query = dim_query

    client.query(merge_query).result()
    client.delete_table(f"pc_part_prices_star.staging_{staging_table_name}", not_found_ok=True)


def write_star_to_bq(df: pd.DataFrame, table: str, schema: list[dict]):
    staging_table_name = get_staging_table_name(table.split(".")[1])

    write_df_to_staging_bq(df, schema, staging_table_name)
    ensure_table_exists(table, schema)
    merge_staging_to_star_table(table, schema, staging_table_name)


def write_all_to_bq(transformed_parts: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame], category: str, part_schema: list[dict]):
    dim_products, dim_specs, fact_prices, fact_vector_search = transformed_parts

    write_star_to_bq(dim_products, "pc_part_prices_star.dim_products", DIM_PRODUCTS_SCHEMA)
    write_star_to_bq(dim_specs, f"pc_part_prices_star.dim_{category}_specs", part_schema)
    write_star_to_bq(fact_prices, "pc_part_prices_star.fact_prices", FACT_PRICES_SCHEMA)
    write_star_to_bq(fact_vector_search, "pc_part_prices_star.fact_vector_search", FACT_VECTOR_SEARCH_SCHEMA)

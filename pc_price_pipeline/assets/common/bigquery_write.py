import os
import pandas as pd
from pandas_gbq import to_gbq, read_gbq
import google.auth

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "pc-price-pipeline")

ENV = "prod" # prod or dev
WRITE_MODE = "replace" if ENV == "dev" else "append"


def write_to_bq(df: pd.DataFrame, table: str, schema: list[dict]):
    if df.empty:
        raise ValueError(f"{table} is empty — aborting BigQuery write")

    credentials, _ = google.auth.default()

    if WRITE_MODE == "append":
        # Query existing data to check for duplicates
        df["scrape_window"] = df["scraped_at"].dt.floor("1H")
        
        try:
            existing = read_gbq(
                f"""
                SELECT DISTINCT
                    raw_name,
                    store, 
                    source_url,
                    TIMESTAMP_TRUNC(scraped_at, HOUR) as scrape_window
                FROM `{table}`
                WHERE DATE(scraped_at) = CURRENT_DATE()
                """,
                project_id=PROJECT_ID,
                credentials=credentials
            )
            
            # Anti-join: keep only new records
            merge_key = ["raw_name", "store", "source_url", "scrape_window"]
            df_new = df.merge(existing, on=merge_key, how="left", indicator=True)
            df_new = df_new[df_new["_merge"] == "left_only"].drop(columns=["_merge"])
            df_new = df_new.drop(columns=["scrape_window"])
            
        except Exception:
            # Table doesn't exist yet or query failed - write all data
            df_new = df.drop(columns=["scrape_window"])
        
        if df_new.empty:
            print(f"No new records to write to {table}")
            return
            
        df = df_new

    to_gbq(
        df,
        destination_table=table,
        project_id=PROJECT_ID,
        table_schema=schema,
        if_exists=WRITE_MODE,
        credentials=credentials,
    )
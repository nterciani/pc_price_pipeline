import pandas as pd
from pandas_gbq import to_gbq

PROJECT_ID = "pc-price-pipeline"

ENV = "prod"  # dev or prod
WRITE_MODE = "replace" if ENV == "dev" else "append"

def write_to_bq(df: pd.DataFrame, table: str, schema: list[dict]):
    if df.empty:
        raise ValueError(f"{table} is empty — aborting BigQuery write")

    to_gbq(
        df,
        destination_table=table,
        project_id=PROJECT_ID,
        table_schema=schema,
        if_exists=WRITE_MODE
    )

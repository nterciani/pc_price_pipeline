import os
import pandas as pd
from pandas_gbq import to_gbq
from google.oauth2 import service_account
import google.auth

# Prefer CI-provided env vars, fallback to default
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "pc-price-pipeline")

ENV = "prod"  # dev or prod
WRITE_MODE = "replace" if ENV == "dev" else "append"


def _load_credentials():
    """Load service-account creds when available to avoid browser auth in CI."""
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if key_path and os.path.exists(key_path):
        return service_account.Credentials.from_service_account_file(key_path)

    credentials, _ = google.auth.default()
    return credentials


def write_to_bq(df: pd.DataFrame, table: str, schema: list[dict]):
    if df.empty:
        raise ValueError(f"{table} is empty — aborting BigQuery write")

    credentials = _load_credentials()

    to_gbq(
        df,
        destination_table=table,
        project_id=PROJECT_ID,
        table_schema=schema,
        if_exists=WRITE_MODE,
        credentials=credentials,
    )

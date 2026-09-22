import os
import pandas as pd
from uuid import uuid4
from functools import lru_cache
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from sentence_transformers import SentenceTransformer
from pc_price_pipeline.assets.common.bigquery_helpers import write_df_to_staging_bq, read_from_gbq_data_set

EMBEDDING_MODEL_NAME = "jinaai/jina-embeddings-v3-hf"
VECTOR_SEARCH_CONFIDENCE_THRESHOLD = 0.01

TEMP_VECTOR_SCHEMA = [
    {"name": "match_id", "type": "STRING"},
    {"name": "product_name", "type": "STRING"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "product_embedding", "type": "FLOAT64", "mode": "REPEATED"},
]


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """ Returns a cached instance of the embedding model. """
    return SentenceTransformer(
        EMBEDDING_MODEL_NAME,
        trust_remote_code=True
    )


def generate_product_embeddings(df: pd.DataFrame) -> pd.DataFrame:
    """ Generates embeddings based on the dataframe's product_name and inserts
    them into a product_embedding column.
    """
    model = get_embedding_model()

    raw_names = df["product_name"].fillna("").tolist()

    embeddings_matrix = model.encode(
        raw_names,
        task="text-matching",
        prompt_name="text-matching",
        normalize_embeddings=True,
    )

    df["product_embedding"] = [vec.tolist() for vec in embeddings_matrix]

    return df


def perform_vector_search(df_intermediate: pd.DataFrame) -> pd.DataFrame | None:
    """ Performs a vector search on the dataframe based on the product_name embeddings and returns a dataframe
    with the most similar product_key along with additional match_confidence, and match_method for each product 
    in the input dataframe. df_intermediate must have match_id and product_embedding columns.
    """
    client = bigquery.Client()

    staging_table_name = f"fact_vector_search_{os.getpid()}_{uuid4().hex}"

    try:
        write_df_to_staging_bq(
            df_intermediate[["match_id", "product_name", "scraped_at", "product_embedding"]],
            TEMP_VECTOR_SCHEMA,
            staging_table_name,
        )
        query = f"""
            SELECT
                query.match_id,
                EXTRACT(DATE FROM query.scraped_at) as match_date,
                query.product_name AS incoming_product_name,
                base.product_name AS database_product_name,
                query.scraped_at,
                false AS is_approved,
                base.product_key,
                distance AS match_confidence,
                'vector_search' AS match_method
            FROM VECTOR_SEARCH(
                TABLE `pc_part_prices_star.dim_products`,
                'product_embedding',
                TABLE `pc_part_prices_star.staging_{staging_table_name}`,
                'product_embedding',
                top_k => 1,
                distance_type => 'COSINE'
            )
        """

        query_job = client.query(query)
        new_df = query_job.to_dataframe()
    finally:
        client.delete_table(f"pc_part_prices_star.staging_{staging_table_name}", not_found_ok=True)

    if new_df.empty:
        return None

    clean_df = new_df[new_df["match_confidence"] <= VECTOR_SEARCH_CONFIDENCE_THRESHOLD]

    return clean_df


def match_intermediate_to_existing_products(df_intermediate: pd.DataFrame) -> pd.DataFrame:
    """ Matches products in an intermediate dataframe to existing products in the dim_products table in gbq. First,
    it checks for exact product_key matches int the dim_products table. If no exact match is found, it performs
    a vector search to find the most similar product in the dim_products table based on the product_name.
    """
    df_intermediate = df_intermediate.copy()

    df_intermediate["source_product_key"] = df_intermediate["product_key"]

    df_intermediate["candidate_product_key"] = None
    df_intermediate["match_confidence"] = 1.0
    df_intermediate["match_method"] = "exact_match"
    df_intermediate["is_approved"] = True

    # check if dim_products table exists
    try:
        bigquery.Client().get_table("pc_part_prices_star.dim_products")
    except NotFound:
        return df_intermediate

    existing_keys = read_from_gbq_data_set(
        "SELECT product_key FROM `pc_part_prices_star.dim_products`"
    )["product_key"].tolist()

    df_existing = df_intermediate[df_intermediate["product_key"].isin(existing_keys)].copy()
    df_missing = df_intermediate[~df_intermediate["product_key"].isin(existing_keys)].copy()

    if df_missing.empty:
        return df_existing

    df_missing["match_id"] = df_missing.index.astype(str)
    vector_results = perform_vector_search(df_missing)

    if vector_results is None or vector_results.empty:
        return pd.concat([df_existing, df_missing], ignore_index=True)

    vector_results.set_index("match_id", inplace=True)

    for idx, row in df_missing.iterrows():
        match_id = str(idx)

        if match_id not in vector_results.index:
            continue

        result = vector_results.loc[match_id]
        distance = float(result["match_confidence"])

        if distance <= VECTOR_SEARCH_CONFIDENCE_THRESHOLD:
            df_missing.at[idx, "candidate_product_key"] = result["product_key"]
            df_missing.at[idx, "match_confidence"] = distance
            df_missing.at[idx, "match_method"] = result["match_method"]
            df_missing.at[idx, "is_approved"] = False
            df_missing.at[idx, "product_key"] = result["product_key"]

    return pd.concat([df_existing, df_missing], ignore_index=True)

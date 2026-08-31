import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from sentence_transformers import SentenceTransformer
from pc_price_pipeline.assets.common.bigquery_helpers import write_df_to_staging_bq, read_from_gbq_data_set

TEMP_VECTOR_SCHEMA = [
    {"name": "match_id", "type": "STRING"},
    {"name": "product_name", "type": "STRING"},
    {"name": "scraped_at", "type": "TIMESTAMP"},
    {"name": "product_embedding", "type": "FLOAT64", "mode": "REPEATED"},
]


def generate_product_embeddings(df: pd.DataFrame) -> pd.DataFrame:
    """ Generates embeddings based on the dataframe's product_name and inserts
    them into a product_embedding column.
    """
    model = SentenceTransformer(
        "jinaai/jina-embeddings-v3-hf", 
        trust_remote_code=True
    )

    df["product_embedding"] = df["product_name"].apply(lambda x: model.encode(x,
                                                                              task="text-matching",
                                                                              prompt_name="text-matching",
                                                                              normalize_embeddings=True
                                                                              ).tolist() if pd.notnull(x) else None)

    return df


def perform_vector_search(df_intermediate: pd.DataFrame) -> pd.DataFrame | None:
    """ Performs a vector search on the dataframe based on the product_name embeddings and returns a dataframe
    with the most similar product_key along with additional match_confidence, and match_method for each product 
    in the input dataframe. df_intermediate must have match_id and product_embedding columns.
    """
    bq_confidence_threshold = 0.95

    client = bigquery.Client()

    write_df_to_staging_bq(df_intermediate[["match_id", "product_name", "scraped_at", "product_embedding"]], TEMP_VECTOR_SCHEMA)

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
            TABLE `pc_part_prices_star.staging`,
            'product_embedding',
            top_k => 1
        )
        
    """

    query_job = client.query(query)
    new_df = query_job.to_dataframe()

    client.delete_table("pc_part_prices_star.staging", not_found_ok=True)

    if new_df.empty:
        return 

    clean_df = new_df[new_df['match_confidence'] >= bq_confidence_threshold]

    return clean_df


def match_intermediate_to_existing_products(df_intermediate: pd.DataFrame) -> pd.DataFrame:
    """ Matches products in an intermediate dataframe to existing products in the dim_products table in gbq. First,
    it checks for exact product_key matches int the dim_products table. If no exact match is found, it performs
    a vector search to find the most similar product in the dim_products table based on the product_name.
    """
    vector_search_columns = ["match_confidence", "match_method", "is_approved"]

    product_keys = df_intermediate["product_key"].tolist()
    keys_string = ", ".join(f"'{key}'" for key in product_keys)

    query = f"""
        SELECT product_key
        FROM `pc_part_prices_star.dim_products`
        WHERE product_key IN ({keys_string})
    """

    df_intermediate[vector_search_columns] = None

    # check if dim_products table exists
    try:
        bigquery.Client().get_table("pc_part_prices_star.dim_products")
    except NotFound:
        return df_intermediate

    df_existing_products = df_intermediate[df_intermediate["product_key"].isin(read_from_gbq_data_set(query)["product_key"])]
    df_non_existing_products = df_intermediate[~df_intermediate["product_key"].isin(df_existing_products["product_key"])].copy()

    if not df_non_existing_products.empty:
        df_non_existing_products["match_id"] = df_non_existing_products.index.astype(str)
        df_vector_search_results = perform_vector_search(df_non_existing_products)

        if df_vector_search_results is not None and not df_vector_search_results.empty:
            # Set match_id as index on the search results for clean mapping
            v_results_indexed = df_vector_search_results.set_index("match_id")

            # Only extract the rows that actually found a vector match
            matched_ids = df_non_existing_products["match_id"].isin(v_results_indexed.index)

            if matched_ids.any():
                # Target only matched rows and map values cleanly by index alignment
                target_indices = df_non_existing_products[matched_ids].index
                target_match_ids = df_non_existing_products.loc[target_indices, "match_id"]

                # Assign values only to the subset that matched
                cols_to_update = vector_search_columns + ["product_key"]
                df_non_existing_products.loc[target_indices, cols_to_update] = v_results_indexed.loc[target_match_ids, cols_to_update].values

    return pd.concat([df_existing_products, df_non_existing_products], ignore_index=True)

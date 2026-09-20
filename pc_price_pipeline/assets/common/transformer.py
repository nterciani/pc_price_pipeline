import pandas as pd
from pc_price_pipeline.assets.common.utils import *
from pc_price_pipeline.assets.common.star_schemas import *
from pc_price_pipeline.assets.common.embedding_and_vectors import generate_product_embeddings, match_intermediate_to_existing_products


class Transformer:
    def __init__(self, df_clean: pd.DataFrame, brand_pattern: str, specs_schema: list[dict]):
        self.df_clean = df_clean
        self.brand_pattern = brand_pattern
        self.specs_schema = specs_schema

    def get_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """Must be implemented per class to extract the product name."""
        raise NotImplementedError("Subclasses must implement get_name()")

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Must be implemented per class to extract the product's specs.""" 
        raise NotImplementedError("Subclasses must implement get_specs()")

    def get_product_key_columns(self, df: pd.DataFrame) -> list[str]:
        return [col["name"] for col in self.specs_schema if col["name"] in df.columns]

    def clean_to_intermediate(self, df_clean: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms clean data in the form of the raw prices schema into a 
        dataframe that can be used to populate a star schema, including a 
        fact table for prices, a dimension table for products and a dimension 
        table for specs.
        """
        df_inter = df_clean.copy()
        
        df_inter = df_inter.rename(columns={"category": "product_category"})

        df_inter["price_date"] = df_inter["scraped_at"]
        df_inter["retailer_key"] = df_inter["store"].apply(generate_retailer_id)

        # get as much info as possible from the raw schema
        df_inter["product_brand"] = df_inter["raw_name"].str.extract(self.brand_pattern).iloc[:, 0]
        df_inter = self.get_specs(df_inter)

        # set empty string entries to none
        df_inter = df_inter.replace(r"^\s*$", None, regex=True)

        df_inter = self.get_name(df_inter)

        # products with no names arent useful
        df_inter = df_inter[df_inter["product_name"].notnull()]

        # make product key from specs
        key_columns = self.get_product_key_columns(df_inter)
        df_inter["product_key"] = df_inter[key_columns].drop("needs_review", axis=1).apply(generate_product_key, axis=1)

        return df_inter

    def intermediate_to_star(self, df_intermediate: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Transforms the intermediate dataframe into a tuple of dataframes that can be used to populate a star schema.
        Returns a tuple of dataframes corresponding to the dim_products, dim_*_specs, 
        fact_prices, and fact_vector_search tables in the star schema.
        """
        # embedding
        df_intermediate = generate_product_embeddings(df_intermediate)

        # vector search and match to existing products
        df_intermediate = match_intermediate_to_existing_products(df_intermediate)

        # Split the intermediate dataframe into dim_products, dim_specs, and fact_prices
        dim_products = df_intermediate[[spec["name"] for spec in DIM_PRODUCTS_SCHEMA]].groupby("product_key").first().reset_index()
        dim_specs = df_intermediate[[spec["name"] for spec in self.specs_schema]].groupby("product_key").first().reset_index()
        fact_prices = df_intermediate[[spec["name"] for spec in FACT_PRICES_SCHEMA]].drop_duplicates(subset=["price_date", "product_key", "retailer_key", "source_url"])
        fact_vector_search = df_intermediate[[spec["name"] for spec in FACT_VECTOR_SEARCH_SCHEMA]].drop_duplicates(subset=["raw_name", "match_confidence", "match_method", "is_approved", "scraped_at"])

        return dim_products, dim_specs, fact_prices, fact_vector_search

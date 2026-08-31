import pandas as pd
from pc_price_pipeline.assets.common.utils import *


class Transformer:
    def __init__(self, df_raw: pd.DataFrame, brand_pattern: str, specs_schema: list[dict]):
        self.df_raw = df_raw
        self.brand_pattern = brand_pattern
        self.specs_schema = specs_schema

    def get_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """Must be implemented per class to extract the product name."""
        raise NotImplementedError("Subclasses must implement get_name()")

    def get_specs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Must be implemented per class to extract the product's specs.""" 
        raise NotImplementedError("Subclasses must implement get_specs()")

    def raw_to_intermediate(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms raw data in the form of the raw prices schema into a 
        dataframe that can be used to populate a star schema, including a 
        fact table for prices, a dimension table for products and a dimension 
        table for specs.
        """
        df_inter = df_raw.copy()
        
        # TODO: raw_price should not be simply renamed after the migration is fully made, but for now
        #       it can be renamed since the "raw_price" has been cleaned.
        df_inter = df_inter.rename(columns={"raw_price": "price", "category": "product_category"})

        df_inter["price_date"] = df_inter["scraped_at"]
        df_inter["retailer_key"] = df_inter["store"].apply(generate_retailer_id)

        # get as much info as possible from the raw schema
        df_inter["product_brand"] = df_inter["raw_name"].str.extract(self.brand_pattern).iloc[:, 0]
        df_inter = self.get_specs(df_inter)
        df_inter = self.get_name(df_inter)

        # make product key from specs
        key_columns = [col["name"] for col in self.specs_schema if col["name"] in df_inter.columns]
        df_inter["product_key"] = df_inter[key_columns].drop("needs_review", axis=1).apply(generate_product_key, axis=1)

        return df_inter
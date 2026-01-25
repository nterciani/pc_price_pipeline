import pandas as pd

def cleaned_prices_df(df: pd.DataFrame, extra_schemas: list=None) -> pd.DataFrame:
    """
    Cleans and validates raw pricing data.
    Removes invalid rows and standardizes formats.
    """
    df = df.copy()

    df["price"] = df["raw_price"]
    df = df.dropna(subset=["price"])
    df = df[df["price"] > 0]

    df["raw_name"] = df["raw_name"].str.replace(r'\s+', ' ', regex=True).str.strip()

    df = df[~df['source_url'].str.contains('ComboDeal', na=False)]

    df["scrape_window"] = df["scraped_at"].dt.floor("1H")

    df = df.drop_duplicates(
        subset=["raw_name", "store", "source_url", "scrape_window"]
    )

    df = df.drop(columns=["scrape_window"])
    
    df = df[
        [
            "raw_name",
            "price",
            "store",
            "category",
            "scraped_at",
            "source_url",
        ] + (extra_schemas if extra_schemas is not None else [])
    ]

    return df

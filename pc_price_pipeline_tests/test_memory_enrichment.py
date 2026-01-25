import pandas as pd
from pc_price_pipeline.assets.memory.enriched import enriched_memory

def test_enriched_memory_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "CORSAIR Vengeance RGB 96GB (4 x 24GB) 288-Pin PC RAM DDR5 6400 (PC5 51200) Desktop Memory",
            "Team Xtreem ARGB 32GB (2 x 16GB) 288-Pin PC RAM DDR5 7200 (PC5 57600) Desktop Memory",
            "Patriot Viper Steel RGB 32GB 288-Pin PC RAM DDR4 3600 (PC4 28800) Desktop Memory Model PVSR432G360C0",
        ],
        "category": ["GPU", "GPU", "GPU"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_memory(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "CORSAIR"
    assert row["memory_type"] == "DDR5"
    assert row["capacity"] == "96GB"
    assert row["speed"] == "6400"
    assert row["modules"] == "4 x 24GB"
    assert row["product_family"] == "CORSAIR DDR5 6400 96GB 4 x 24GB"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "TEAM GROUP"
    assert row2["memory_type"] == "DDR5"
    assert row2["capacity"] == "32GB"
    assert row2["speed"] == "7200"
    assert row2["modules"] == "2 x 16GB"
    assert row2["product_family"] == "TEAM GROUP DDR5 7200 32GB 2 x 16GB"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "PATRIOT"
    assert row3["memory_type"] == "DDR4"
    assert row3["capacity"] == "32GB"
    assert row3["speed"] == "3600"
    assert pd.isna(row3["modules"]) 
    assert row3["product_family"] == "PATRIOT DDR4 3600 32GB"
    assert isinstance(row3["product_id"], str)

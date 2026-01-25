import pandas as pd
from pc_price_pipeline.assets.gpu.enriched import enriched_gpus

def test_enriched_gpus_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "ASRock Challenger Arc B570 10GB GDDR6 PCI Express 4.0 x8 ATX Graphics Card B570 CL 10GO",
            "Refurbished ASUS TUF Gaming GeForce RTX 3080 TUF-RTX3080-O10G-GAMING Video Card",
            "Refurbished SAPPHIRE PULSE Radeon RX 6750 XT 12GB GDDR6 PCI Express 4.0 ATX Graphics Card",
        ],
        "category": ["GPU", "GPU", "GPU"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_gpus(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "ASROCK"
    assert row["chipset"] == "ARC B570"
    assert row["memory"] == "10GB"
    assert row["memory_type"] == "GDDR6"
    assert row["product_family"] == "ASROCK ARC B570 10GB"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "ASUS"
    assert row2["chipset"] == "GEFORCE RTX 3080"
    assert row2["memory"] == "10GB"
    assert row2["memory_type"] is None
    assert row2["product_family"] == "ASUS GEFORCE RTX 3080 10GB"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "SAPPHIRE"
    assert row3["chipset"] == "RADEON RX 6750 XT"
    assert row3["memory"] == "12GB"
    assert row3["memory_type"] == "GDDR6"
    assert row3["product_family"] == "SAPPHIRE RADEON RX 6750 XT 12GB"
    assert isinstance(row3["product_id"], str)

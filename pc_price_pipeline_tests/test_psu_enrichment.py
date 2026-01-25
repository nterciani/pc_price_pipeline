import pandas as pd
from pc_price_pipeline.assets.psu.enriched import enriched_psus

def test_enriched_psu_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "Phanteks AMP GH 1200W Platinum Power Supply, ATX 3.1 and PCIe 5.1 Platform, Fully Modular Individual Cables, Silent Fanless mode",
            "ASUS ROG Loki SFX-L 1200W Titanium PSU (Fully Modular Power Supply, 80+ Titanium, 120mm PWM ARGB Fan, Aura Sync)",
            "Corsair CX650M (2025) Semi Modular ATX 3.1 PCIe 5.1 Low-Noise 650W Power Supply with 12V-2x6 Cable – Cybenetics Bronze Efficiency",
        ],
        "category": ["GPU", "GPU", "GPU"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_psus(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "PHANTEKS"
    assert row["psu_type"] == "ATX"
    assert row["efficiency_rating"] == "80+ PLATINUM"
    assert row["wattage"] == "1200W"
    assert row["modular"] == True
    assert row["product_family"] == "PHANTEKS 1200W 80+ PLATINUM ATX"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "ASUS"
    assert row2["psu_type"] == "SFX-L"
    assert row2["efficiency_rating"] == "80+ TITANIUM"
    assert row2["wattage"] == "1200W"
    assert row2["modular"] == True
    assert row2["product_family"] == "ASUS 1200W 80+ TITANIUM SFX-L"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "CORSAIR"
    assert row3["psu_type"] == "ATX"
    assert row3["efficiency_rating"] == "CYBENETICS BRONZE"
    assert row3["wattage"] == "650W"
    assert row3["modular"] == True
    assert row3["product_family"] == "CORSAIR 650W CYBENETICS BRONZE ATX"
    assert isinstance(row3["product_id"], str)

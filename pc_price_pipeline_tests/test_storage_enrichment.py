import pandas as pd
from pc_price_pipeline.assets.storage.enriched import enriched_storage

def test_enriched_storage_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "Micron 5400 MAX - SSD - 480 GB - internal - 2.5\" - SATA 6Gb/s",
            "Corsair MP700 Elite M.2 2280 1TB PCI-Express 5.0 x4 3D TLC Internal Solid State Drive (SSD) Up to 10000 MB/s",
            "Crucial P310 M.2 2280 4TB PCI-Express 4.0 x4 NVMe 3D NAND Internal Solid State Drive (SSD)",
        ],
        "category": ["GPU", "GPU", "GPU"],
        "storage_type": ["SSD", "SSD", "SSD"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_storage(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "MICRON"
    assert row["capacity"] == "480GB"
    assert row["storage_type"] == "SSD"
    assert row["form_factor"] == "2.5\""
    assert row["interface"] == "SATA"
    assert row["product_family"] == "MICRON 480GB 2.5\" SATA SSD"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "CORSAIR"
    assert row2["capacity"] == "1TB"
    assert row2["storage_type"] == "SSD"
    assert row2["form_factor"] == "M.2 2280"
    assert row2["interface"] == "PCIE 5.0 X4"
    assert row2["product_family"] == "CORSAIR 1TB M.2 2280 PCIE 5.0 X4 SSD"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "CRUCIAL"
    assert row3["capacity"] == "4TB"
    assert row3["storage_type"] == "SSD"
    assert row3["form_factor"] == "M.2 2280"
    assert row3["interface"] == "PCIE 4.0 X4"
    assert row3["product_family"] == "CRUCIAL 4TB M.2 2280 PCIE 4.0 X4 SSD"
    assert isinstance(row3["product_id"], str)

import pandas as pd
from pc_price_pipeline.assets.mobo.enriched import enriched_mobos

def test_enriched_mobos_basic_extraction():
    df = pd.DataFrame({
        "raw_name": [
            "MSI MAG B550 TOMAHAWK MAX WIFI, AMD B550 ATX AM4, 4 Dimm DDR4, PCIE 4.0, M.2 x 2, USB 3.2 Ports, JRGB JRAINBOW, WIFI 6",
            "ASRock B850M-X R2.0 AM5 Micro-ATX Motherboard: AMD Ryzen 9000/8000/7000 Ready | DDR5 8200+ OC | PCIe 5.0 M.2",
            "MSI MAG B860 TOMAHAWK WIFI LGA 1851 Intel B860 SATA 6Gb/s Intel Core Ultra DDR5 ATX Motherboard",
        ],
        "category": ["GPU", "GPU", "GPU"],
        "store": ["newegg", "newegg", "newegg"],
        "price": [199.99, 309.99, 549.99],
        "scraped_at": ["2026-01-01", "2026-01-20", "2026-01-25"],
        "source_url": ["https://newegg.com/example", "https://newegg.com/example2", "https://newegg.com/example3"]
    })

    result = enriched_mobos(df)

    row = result.iloc[0]
    row2 = result.iloc[1]
    row3 = result.iloc[2]

    assert row["brand"] == "MSI"
    assert row["socket"] == "AM4"
    assert row["form_factor"] == "ATX"
    assert row["chipset"] == "B550"
    assert row["memory_type"] == "DDR4"
    assert row["wifi"] == True
    assert row["product_family"] == "MSI B550 AM4 ATX"
    assert isinstance(row["product_id"], str)

    assert row2["brand"] == "ASROCK"
    assert row2["socket"] == "AM5"
    assert row2["form_factor"] == "MICRO ATX"
    assert row2["chipset"] == "B850"
    assert row2["memory_type"] == "DDR5"
    assert row2["wifi"] == False
    assert row2["product_family"] == "ASROCK B850 AM5 MICRO ATX"
    assert isinstance(row2["product_id"], str)

    assert row3["brand"] == "MSI"
    assert row3["socket"] == "LGA 1851"
    assert row3["form_factor"] == "ATX"
    assert row3["chipset"] == "B860"
    assert row3["memory_type"] == "DDR5"
    assert row3["wifi"] == True
    assert row3["product_family"] == "MSI B860 LGA 1851 ATX"
    assert isinstance(row3["product_id"], str)

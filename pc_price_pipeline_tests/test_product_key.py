import pandas as pd

from pc_price_pipeline.assets.common.utils import generate_product_key, generate_retailer_id

def test_product_key_is_deterministic():
    specs = pd.Series(["AMD", "RYZEN 5 5600X", "AM4"])

    id1 = generate_product_key(specs)
    id2 = generate_product_key(specs)

    assert id1 == id2

def test_product_key_changes_when_specs_change():
    assert generate_product_key(pd.Series(["AMD", "RYZEN 5 5600X"])) != generate_product_key(
        pd.Series(["AMD", "RYZEN 7 5800X"])
    )


def test_retailer_key_uses_canonical_newegg_key():
    assert generate_retailer_id("Newegg") == "newegg"

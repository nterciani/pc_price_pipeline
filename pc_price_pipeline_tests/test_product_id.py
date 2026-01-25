from pc_price_pipeline.assets.common.utils import generate_product_id

def test_product_id_is_deterministic():
    name = "Ryzen 5 5600X"

    id1 = generate_product_id(name)
    id2 = generate_product_id(name)

    assert id1 == id2

def test_product_id_differs_for_different_products():
    assert generate_product_id("Ryzen 5 5600X") != generate_product_id("Ryzen 7 5800X")

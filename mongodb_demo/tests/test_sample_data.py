from mongodb_demo.backend.sample_data import PRODUCT_TYPES, SAMPLE_PRODUCTS_BY_TYPE, generate_products


def test_generated_products_cover_all_product_types_and_schema_versions():
    products = generate_products(count=50)
    product_types = {product["productType"] for product in products}
    schema_versions = {product["schemaVersion"] for product in products}

    assert product_types == set(PRODUCT_TYPES)
    assert schema_versions == {1, 2}
    assert any("regionalTaxCode" in product for product in products)
    assert any("regionalTaxCode" not in product for product in products)
    assert all("shipping" not in product for product in products)
    assert all("tags" not in product for product in products)


def test_prepared_sample_exists_for_each_product_family():
    assert set(SAMPLE_PRODUCTS_BY_TYPE) == set(PRODUCT_TYPES)
    assert all(product["regionalTaxCode"] == "DE-STD" for product in SAMPLE_PRODUCTS_BY_TYPE.values())
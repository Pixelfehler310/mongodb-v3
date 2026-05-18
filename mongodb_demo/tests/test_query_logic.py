from mongodb_demo.backend.query_logic import build_aggregation_pipeline, build_product_query


def test_combined_product_query_contains_simple_nested_and_evolution_filters():
    product_query = build_product_query(
        {
            "productType": "laptop",
            "manufacturer": "Northstar Computing",
            "category": "laptops",
            "minPrice": "900",
            "maxPrice": "1800",
            "ramMin": "32",
            "schemaEvolution": "withTaxCode",
            "search": "pro",
        },
        default_limit=25,
    )

    assert product_query.query["productType"] == "laptop"
    assert product_query.query["manufacturer.name"] == "Northstar Computing"
    assert product_query.query["categories.slug"] == "laptops"
    assert product_query.query["basePrice"] == {"$gte": 900.0, "$lte": 1800.0}
    assert product_query.query["attributes.ramGb"] == {"$gte": 32}
    assert product_query.query["regionalTaxCode"] == {"$exists": True}
    assert "$or" in product_query.query


def test_aggregation_pipeline_for_manufacturer_ratings_unwinds_review_array():
    pipeline = build_aggregation_pipeline("avgRatingByManufacturer")

    assert pipeline[0] == {"$unwind": "$latestReviews"}
    assert pipeline[1]["$group"]["_id"] == "$manufacturer.name"
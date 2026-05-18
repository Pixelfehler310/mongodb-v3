import pytest

from mongodb_demo.backend.product_contract import ProductValidationError, normalize_product_payload
from mongodb_demo.backend.sample_data import build_live_sample


def test_normalize_product_payload_generates_missing_ids_and_timestamps():
    payload = build_live_sample("laptop", 42)
    payload.pop("_id")
    payload.pop("productId")
    payload.pop("createdAt")
    payload.pop("updatedAt")

    product = normalize_product_payload(payload)

    assert product["_id"].startswith("prod_")
    assert product["productId"] == product["_id"]
    assert product["createdAt"].endswith("Z")
    assert product["updatedAt"].endswith("Z")


def test_normalize_product_payload_preserves_existing_identity_on_replace():
    existing = build_live_sample("book", 1)
    payload = build_live_sample("book", 2)
    payload["_id"] = "attempted_new_id"
    payload["productId"] = "attempted_new_product_id"
    payload["name"] = "Updated Book"

    product = normalize_product_payload(payload, existing=existing)

    assert product["_id"] == existing["_id"]
    assert product["productId"] == existing["productId"]
    assert product["createdAt"] == existing["createdAt"]
    assert product["name"] == "Updated Book"


def test_normalize_product_payload_reports_invalid_nested_fields():
    payload = build_live_sample("t-shirt", 1)
    payload["manufacturer"] = {"id": "", "name": ""}
    payload["categories"] = []
    payload["latestReviews"] = [{"reviewId": "rev_bad", "rating": 8, "title": "Too high"}]

    with pytest.raises(ProductValidationError) as error:
        normalize_product_payload(payload)

    assert "manufacturer.id is required." in error.value.errors
    assert "categories must be a non-empty array." in error.value.errors
    assert "latestReviews[0].rating must be an integer from 1 to 5." in error.value.errors
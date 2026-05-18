from __future__ import annotations

import copy
import re
import uuid
from datetime import datetime, timezone
from typing import Any


class ProductValidationError(ValueError):
    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


class ProductConflictError(ValueError):
    pass


def normalize_product_payload(payload: Any, *, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ProductValidationError(["Request body must be a JSON object."])

    product = copy.deepcopy(payload)
    errors: list[str] = []
    now = _utc_now()

    if existing is None:
        product_id = _clean_text(product.get("_id") or product.get("productId")) or f"prod_{uuid.uuid4().hex[:10]}"
        product["_id"] = product_id
        product["productId"] = _clean_text(product.get("productId")) or product_id
        product["createdAt"] = _clean_text(product.get("createdAt")) or now
    else:
        product["_id"] = existing["_id"]
        product["productId"] = existing.get("productId") or existing["_id"]
        product["createdAt"] = existing.get("createdAt") or _clean_text(product.get("createdAt")) or now

    product["updatedAt"] = now
    product["sku"] = _required_text(product, "sku", errors)
    product["productType"] = _required_text(product, "productType", errors)
    product["name"] = _required_text(product, "name", errors)
    product["currency"] = _clean_text(product.get("currency")) or "EUR"
    product["status"] = _clean_text(product.get("status")) or "available"
    product["basePrice"] = _required_number(product, "basePrice", errors)
    product["schemaVersion"] = _required_int(product, "schemaVersion", errors, default=2)

    # Lazy Migration: Ensure regionalTaxCode exists with a default value
    product["regionalTaxCode"] = _clean_text(product.get("regionalTaxCode")) or "DE-STD"

    if "source" in product and product["source"] is not None:
        product["source"] = _clean_text(product["source"])

    product["manufacturer"] = _manufacturer(product.get("manufacturer"), errors)
    product["categories"] = _categories(product.get("categories"), errors)
    product["attributes"] = _attributes(product.get("attributes"), errors)
    product["variants"] = _variants(product.get("variants"), errors)
    product["highlights"] = _highlights(product.get("highlights"), errors)
    product["latestReviews"] = _reviews(product.get("latestReviews"), errors)

    if errors:
        raise ProductValidationError(errors)
    return product


def _manufacturer(value: Any, errors: list[str]) -> dict[str, str]:
    if not isinstance(value, dict):
        errors.append("manufacturer must be an object with id and name.")
        return {"id": "", "name": ""}
    manufacturer_id = _clean_text(value.get("id"))
    name = _clean_text(value.get("name"))
    if not manufacturer_id:
        errors.append("manufacturer.id is required.")
    if not name:
        errors.append("manufacturer.name is required.")
    return {"id": manufacturer_id, "name": name}


def _categories(value: Any, errors: list[str]) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        errors.append("categories must be a non-empty array.")
        return []
    categories: list[dict[str, str]] = []
    for index, category in enumerate(value):
        if not isinstance(category, dict):
            errors.append(f"categories[{index}] must be an object.")
            continue
        category_id = _clean_text(category.get("id"))
        name = _clean_text(category.get("name"))
        slug = _clean_text(category.get("slug")) or _slugify(name)
        if not category_id:
            errors.append(f"categories[{index}].id is required.")
        if not name:
            errors.append(f"categories[{index}].name is required.")
        if not slug:
            errors.append(f"categories[{index}].slug is required.")
        categories.append({"id": category_id, "name": name, "slug": slug})
    return categories


def _attributes(value: Any, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append("attributes must be an object.")
        return {}
    attributes: dict[str, Any] = {}
    for key, attribute_value in value.items():
        attribute_key = _clean_text(key)
        if not attribute_key:
            errors.append("attributes may not contain an empty key.")
            continue
        if not isinstance(attribute_value, (str, int, float, bool)) or attribute_value is None:
            errors.append(f"attributes.{attribute_key} must be a string, number, or boolean.")
            continue
        attributes[attribute_key] = attribute_value
    return attributes


def _variants(value: Any, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append("variants must be an array.")
        return []
    variants: list[dict[str, Any]] = []
    for index, variant in enumerate(value):
        if not isinstance(variant, dict):
            errors.append(f"variants[{index}] must be an object.")
            continue
        variant_id = _clean_text(variant.get("variantId"))
        label = _clean_text(variant.get("label"))
        inventory_count = _int_value(variant.get("inventoryCount"))
        if not variant_id:
            errors.append(f"variants[{index}].variantId is required.")
        if not label:
            errors.append(f"variants[{index}].label is required.")
        if inventory_count is None:
            errors.append(f"variants[{index}].inventoryCount must be an integer.")
            inventory_count = 0
        variants.append({"variantId": variant_id, "label": label, "inventoryCount": inventory_count})
    return variants


def _highlights(value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append("highlights must be an array.")
        return []
    highlights: list[str] = []
    for index, highlight in enumerate(value):
        text = _clean_text(highlight)
        if not text:
            errors.append(f"highlights[{index}] must be a non-empty string.")
            continue
        highlights.append(text)
    return highlights


def _reviews(value: Any, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append("latestReviews must be an array.")
        return []
    reviews: list[dict[str, Any]] = []
    for index, review in enumerate(value):
        if not isinstance(review, dict):
            errors.append(f"latestReviews[{index}] must be an object.")
            continue
        review_id = _clean_text(review.get("reviewId"))
        title = _clean_text(review.get("title"))
        rating = _int_value(review.get("rating"))
        if not review_id:
            errors.append(f"latestReviews[{index}].reviewId is required.")
        if not title:
            errors.append(f"latestReviews[{index}].title is required.")
        if rating is None or rating < 1 or rating > 5:
            errors.append(f"latestReviews[{index}].rating must be an integer from 1 to 5.")
            rating = 1
        reviews.append({"reviewId": review_id, "rating": rating, "title": title})
    return reviews


def _required_text(product: dict[str, Any], field_name: str, errors: list[str]) -> str:
    value = _clean_text(product.get(field_name))
    if not value:
        errors.append(f"{field_name} is required.")
    return value


def _required_number(product: dict[str, Any], field_name: str, errors: list[str]) -> int | float:
    value = product.get(field_name)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{field_name} must be a number.")
        return 0
    return value


def _required_int(product: dict[str, Any], field_name: str, errors: list[str], *, default: int) -> int:
    value = product.get(field_name, default)
    parsed_value = _int_value(value)
    if parsed_value is None:
        errors.append(f"{field_name} must be an integer.")
        return default
    return parsed_value


def _int_value(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
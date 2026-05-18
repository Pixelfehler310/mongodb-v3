from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
from typing import Any


PRODUCT_TYPES = ["laptop", "t-shirt", "book"]
STATUSES = ["available", "limited", "out_of_stock"]
TAX_CODES = ["DE-STD", "DE-REDUCED", "EU-DIGITAL"]

MANUFACTURERS = {
    "man_northstar": {"id": "man_northstar", "name": "Northstar Computing"},
    "man_urban": {"id": "man_urban", "name": "Urban Loom"},
    "man_atlas": {"id": "man_atlas", "name": "Atlas Academic Press"},
    "man_juniper": {"id": "man_juniper", "name": "Juniper Goods"},
}

CATEGORIES = {
    "cat_laptops": {"id": "cat_laptops", "name": "Laptops", "slug": "laptops"},
    "cat_shirts": {"id": "cat_shirts", "name": "T-Shirts", "slug": "t-shirts"},
    "cat_books": {"id": "cat_books", "name": "Books", "slug": "books"},
    "cat_students": {"id": "cat_students", "name": "Student Picks", "slug": "student-picks"},
    "cat_work": {"id": "cat_work", "name": "Work Essentials", "slug": "work-essentials"},
}

PRODUCT_BLUEPRINTS: list[dict[str, Any]] = [
    {
        "productType": "laptop",
        "skuPrefix": "LAP",
        "name": "Northbook Pro 14",
        "basePrice": 1499.00,
        "manufacturer": MANUFACTURERS["man_northstar"],
        "categories": [CATEGORIES["cat_laptops"], CATEGORIES["cat_work"]],
        "attributes": {"cpuModel": "Ryzen 7 8840U", "ramGb": 32, "storageGb": 1000},
        "variants": [
            {"variantId": "var_16_512", "label": "16 GB / 512 GB", "inventoryCount": 18},
            {"variantId": "var_32_1tb", "label": "32 GB / 1 TB", "inventoryCount": 7},
        ],
        "highlights": ["portable", "developer ready", "quiet"],
        "latestReviews": [
            {"reviewId": "rev_laptop_1", "rating": 5, "title": "Fast and quiet"},
            {"reviewId": "rev_laptop_2", "rating": 4, "title": "Good keyboard"},
        ],
        "status": "available",
    },
    {
        "productType": "t-shirt",
        "skuPrefix": "TSH",
        "name": "Urban Loom Everyday Tee",
        "basePrice": 34.90,
        "manufacturer": MANUFACTURERS["man_urban"],
        "categories": [CATEGORIES["cat_shirts"], CATEGORIES["cat_students"]],
        "attributes": {"size": "M", "material": "organic cotton", "fit": "regular"},
        "variants": [
            {"variantId": "var_black_m", "label": "Black / M", "inventoryCount": 54},
            {"variantId": "var_white_l", "label": "White / L", "inventoryCount": 33},
        ],
        "highlights": ["organic cotton", "student favorite", "washable"],
        "latestReviews": [
            {"reviewId": "rev_shirt_1", "rating": 4, "title": "Comfortable"},
            {"reviewId": "rev_shirt_2", "rating": 5, "title": "Great fit"},
        ],
        "status": "limited",
    },
    {
        "productType": "book",
        "skuPrefix": "BOK",
        "name": "Readable Data Models",
        "basePrice": 49.00,
        "manufacturer": MANUFACTURERS["man_atlas"],
        "categories": [CATEGORIES["cat_books"], CATEGORIES["cat_work"]],
        "attributes": {"author": "Mira Klein", "pageCount": 312, "format": "paperback"},
        "variants": [
            {"variantId": "var_paperback", "label": "Paperback", "inventoryCount": 41},
            {"variantId": "var_ebook", "label": "Ebook", "inventoryCount": 999},
        ],
        "highlights": ["architecture", "schema design", "case studies"],
        "latestReviews": [
            {"reviewId": "rev_book_1", "rating": 5, "title": "Clear examples"},
            {"reviewId": "rev_book_2", "rating": 4, "title": "Useful comparison"},
        ],
        "status": "available",
    },
]


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_product(index: int) -> dict[str, Any]:
    blueprint = PRODUCT_BLUEPRINTS[index % len(PRODUCT_BLUEPRINTS)]
    product_id = f"prod_{1000 + index}"
    updated_at = datetime(2026, 5, 17, 12, 0, tzinfo=timezone.utc) - timedelta(hours=index)
    created_at = updated_at - timedelta(days=21 + index)
    schema_version = 1 if index % 4 == 0 else 2

    document: dict[str, Any] = {
        "_id": product_id,
        "productId": product_id,
        "sku": f"{blueprint['skuPrefix']}-{1000 + index}",
        "productType": blueprint["productType"],
        "name": f"{blueprint['name']} #{index + 1}",
        "basePrice": round(float(blueprint["basePrice"]) + (index % 5) * 7.5, 2),
        "currency": "EUR",
        "manufacturer": copy.deepcopy(blueprint["manufacturer"]),
        "categories": copy.deepcopy(blueprint["categories"]),
        "attributes": copy.deepcopy(blueprint["attributes"]),
        "variants": copy.deepcopy(blueprint["variants"]),
        "highlights": list(blueprint["highlights"]),
        "latestReviews": copy.deepcopy(blueprint["latestReviews"]),
        "status": blueprint["status"],
        "schemaVersion": schema_version,
        "createdAt": _iso(created_at),
        "updatedAt": _iso(updated_at),
    }
    if schema_version == 2:
        document["regionalTaxCode"] = TAX_CODES[index % len(TAX_CODES)]
    return document


def generate_products(count: int = 24, seed: int | None = None) -> list[dict[str, Any]]:
    _ = seed
    return [build_product(index) for index in range(count)]


def build_live_sample(product_type: str = "laptop", sequence: int = 1) -> dict[str, Any]:
    if product_type not in PRODUCT_TYPES:
        product_type = "laptop"
    blueprint_index = PRODUCT_TYPES.index(product_type)
    document = build_product(8000 + blueprint_index + sequence)
    product_id = f"sample_{product_type.replace('-', '_')}_{sequence:03d}"
    now = _iso(datetime.now(timezone.utc))
    document.update(
        {
            "_id": product_id,
            "productId": product_id,
            "sku": f"SMP-{product_type[:3].upper()}-{sequence:03d}",
            "name": f"Live Demo {product_type.title()} {sequence:03d}",
            "source": "live-sample",
            "schemaVersion": 2,
            "regionalTaxCode": "DE-STD",
            "createdAt": now,
            "updatedAt": now,
        }
    )
    return document


SAMPLE_PRODUCTS_BY_TYPE = {product_type: build_live_sample(product_type, 1) for product_type in PRODUCT_TYPES}
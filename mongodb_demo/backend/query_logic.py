from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


AGGREGATIONS = {
    "avgPriceByType": "Average price by product type",
    "countByManufacturer": "Product count by manufacturer",
    "countByCategory": "Product count by category",
    "avgRatingByType": "Average rating by product type",
}


@dataclass(frozen=True)
class ProductQuery:
    query: dict[str, Any]
    sort: dict[str, int]
    limit: int
    filters: dict[str, Any]


def _text(params: Mapping[str, Any], name: str) -> str | None:
    value = params.get(name)
    if value is None:
        return None
    if isinstance(value, list):
        value = value[0] if value else None
    value = str(value).strip()
    return value or None


def _float(params: Mapping[str, Any], name: str) -> float | None:
    value = _text(params, name)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _int(params: Mapping[str, Any], name: str) -> int | None:
    value = _text(params, name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def build_product_query(params: Mapping[str, Any], default_limit: int = 25) -> ProductQuery:
    query: dict[str, Any] = {}
    filters: dict[str, Any] = {}

    exact_fields = {
        "productType": "productType",
        "manufacturer": "manufacturer.name",
        "category": "categories.slug",
        "status": "status",
        "shippingRegion": "shipping.availableRegions",
        "tag": "tags",
    }
    for param_name, field_name in exact_fields.items():
        value = _text(params, param_name)
        if value:
            query[field_name] = value
            filters[param_name] = value

    min_price = _float(params, "minPrice")
    max_price = _float(params, "maxPrice")
    if min_price is not None or max_price is not None:
        price_filter: dict[str, float] = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
            filters["minPrice"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
            filters["maxPrice"] = max_price
        query["basePrice"] = price_filter

    ram_min = _int(params, "ramMin")
    if ram_min is not None:
        query["attributes.ramGb"] = {"$gte": ram_min}
        filters["ramMin"] = ram_min

    schema_evolution = _text(params, "schemaEvolution")
    if schema_evolution == "withTaxCode":
        query["regionalTaxCode"] = {"$exists": True}
        filters["schemaEvolution"] = schema_evolution
    elif schema_evolution == "withoutTaxCode":
        query["regionalTaxCode"] = {"$exists": False}
        filters["schemaEvolution"] = schema_evolution

    search = _text(params, "search")
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"highlights": {"$regex": search, "$options": "i"}},
        ]
        filters["search"] = search

    limit = _int(params, "limit") or default_limit
    limit = max(1, min(limit, 100))

    return ProductQuery(query=query, sort={"updatedAt": -1}, limit=limit, filters=filters)


def build_aggregation_pipeline(kind: str) -> list[dict[str, Any]]:
    if kind == "countByManufacturer":
        return [
            {"$group": {"_id": "$manufacturer.name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
            {"$limit": 12},
        ]
    if kind == "countByCategory":
        return [
            {"$unwind": "$categories"},
            {"$group": {"_id": "$categories.name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
            {"$limit": 12},
        ]
    if kind == "avgRatingByType":
        return [
            {"$unwind": "$latestReviews"},
            {
                "$group": {
                    "_id": "$productType",
                    "averageRating": {"$avg": "$latestReviews.rating"},
                    "reviewCount": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
    return [
        {
            "$group": {
                "_id": "$productType",
                "averagePrice": {"$avg": "$basePrice"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]


def aggregation_label(kind: str) -> str:
    return AGGREGATIONS.get(kind, AGGREGATIONS["avgPriceByType"])
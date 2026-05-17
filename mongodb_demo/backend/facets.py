from __future__ import annotations

from typing import Any

from .query_logic import AGGREGATIONS
from .sample_data import PRODUCT_TYPES, STATUSES


def build_facets(collection: Any) -> dict[str, Any]:
    categories = list(
        collection.aggregate(
            [
                {"$unwind": "$categories"},
                {"$group": {"_id": "$categories.slug", "name": {"$first": "$categories.name"}}},
                {"$sort": {"name": 1}},
            ]
        )
    )
    return {
        "productTypes": sorted(collection.distinct("productType")) or PRODUCT_TYPES,
        "manufacturers": sorted(collection.distinct("manufacturer.name")),
        "categories": [{"slug": item["_id"], "name": item["name"]} for item in categories],
        "statuses": sorted(collection.distinct("status")) or STATUSES,
        "tags": sorted(collection.distinct("tags")),
        "shippingRegions": sorted(collection.distinct("shipping.availableRegions")),
        "ramOptions": sorted(value for value in collection.distinct("attributes.ramGb") if isinstance(value, int)),
        "schemaEvolution": [
            {"value": "withTaxCode", "label": "with regionalTaxCode"},
            {"value": "withoutTaxCode", "label": "without regionalTaxCode"},
        ],
        "aggregations": [{"kind": key, "label": value} for key, value in AGGREGATIONS.items()],
    }
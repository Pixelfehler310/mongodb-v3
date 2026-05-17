from __future__ import annotations

import json
from typing import Any


def _pretty(document: Any) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False)


def format_find_query(query: dict[str, Any], sort: dict[str, int], limit: int) -> str:
    return (
        "db.products.find("
        + _pretty(query)
        + ")\n  .sort("
        + _pretty(sort)
        + f")\n  .limit({limit})"
    )


def format_find_code(query: dict[str, Any], sort: dict[str, int], limit: int) -> str:
    sort_items = list(sort.items())
    return (
        "query = "
        + _pretty(query)
        + "\n\n"
        + f"products = list(collection.find(query).sort({sort_items!r}).limit({limit}))"
    )


def format_detail_query(product_id: str) -> str:
    return f"db.products.findOne({{\n  \"_id\": \"{product_id}\"\n}})"


def format_detail_code(product_id: str) -> str:
    return f"product = collection.find_one({{'_id': '{product_id}'}})"


def format_aggregation_query(pipeline: list[dict[str, Any]]) -> str:
    return "db.products.aggregate(" + _pretty(pipeline) + ")"


def format_aggregation_code(pipeline: list[dict[str, Any]]) -> str:
    return "pipeline = " + _pretty(pipeline) + "\n\nresults = list(collection.aggregate(pipeline))"


def format_insert_query(product_id: str) -> str:
    return f"db.products.insertOne({{ \"_id\": \"{product_id}\", ... }})"


def format_insert_code(product_id: str) -> str:
    return f"collection.insert_one(build_sample_product(product_id='{product_id}'))"
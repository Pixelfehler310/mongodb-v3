from __future__ import annotations

from typing import Any

from .query_logic import build_aggregation_pipeline
from .sample_data import build_live_sample


class ProductRepository:
    def __init__(self, collection: Any):
        self.collection = collection

    def list_products(self, query: dict[str, Any], sort: dict[str, int], limit: int) -> tuple[list[dict[str, Any]], int]:
        cursor = self.collection.find(query).sort(list(sort.items())).limit(limit)
        return list(cursor), self.collection.count_documents(query)

    def get_product(self, product_id: str) -> dict[str, Any] | None:
        return self.collection.find_one({"_id": product_id}) or self.collection.find_one({"productId": product_id})

    def aggregate(self, kind: str) -> list[dict[str, Any]]:
        return list(self.collection.aggregate(build_aggregation_pipeline(kind)))

    def insert_sample_product(self, product_type: str) -> dict[str, Any]:
        sequence = self.collection.count_documents({"source": "live-sample"}) + 1
        document = build_live_sample(product_type=product_type, sequence=sequence)
        self.collection.insert_one(document)
        return document

    def product_count(self) -> int:
        return self.collection.count_documents({})
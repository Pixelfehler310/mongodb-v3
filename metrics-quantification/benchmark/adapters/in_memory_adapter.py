from __future__ import annotations

from collections import defaultdict
from typing import Any

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.seed.generator import Catalog


class InMemoryAdapter(BenchmarkAdapter):
    def __init__(self, database_type: str) -> None:
        self.database_type = database_type
        self.catalog: Catalog | None = None
        self.products_by_id: dict[str, dict[str, Any]] = {}
        self.categories_by_id: dict[str, dict[str, Any]] = {}
        self.manufacturers_by_id: dict[str, dict[str, Any]] = {}
        self.variants_by_product: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.reviews_by_product: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def connect(self) -> None:
        return None

    def close(self) -> None:
        return None

    def reset(self) -> None:
        self.catalog = None
        self.products_by_id.clear()
        self.categories_by_id.clear()
        self.manufacturers_by_id.clear()
        self.variants_by_product.clear()
        self.reviews_by_product.clear()

    def seed(self, catalog: Catalog) -> None:
        self.catalog = catalog
        self.products_by_id = {item["product_id"]: dict(item) for item in catalog.products}
        self.categories_by_id = {item["category_id"]: dict(item) for item in catalog.categories}
        self.manufacturers_by_id = {item["manufacturer_id"]: dict(item) for item in catalog.manufacturers}
        for variant in catalog.variants:
            self.variants_by_product[variant["product_id"]].append(dict(variant))
        for review in catalog.reviews:
            self.reviews_by_product[review["product_id"]].append(dict(review))

    def validate(self, expected_counts: dict[str, int]) -> list[str]:
        actual = {
            "products": len(self.products_by_id),
            "variants": sum(len(items) for items in self.variants_by_product.values()),
            "reviews": sum(len(items) for items in self.reviews_by_product.values()),
            "categories": len(self.categories_by_id),
            "manufacturers": len(self.manufacturers_by_id),
        }
        return [f"{key}: expected {value}, got {actual[key]}" for key, value in expected_counts.items() if actual[key] != value]

    def sample_product_ids(self, limit: int) -> list[str]:
        return list(self.products_by_id.keys())[:limit]

    def sample_category_ids(self, limit: int) -> list[str]:
        return list(self.categories_by_id.keys())[:limit]

    def read_product_aggregate(self, product_id: str) -> dict[str, Any] | None:
        product = self.products_by_id.get(product_id)
        if product is None:
            return None
        category_ids = product["category_ids"]
        return {
            **product,
            "manufacturer": self.manufacturers_by_id.get(product["manufacturer_id"]),
            "categories": [self.categories_by_id[item] for item in category_ids],
            "variants": self.variants_by_product[product_id],
            "recent_reviews": self.reviews_by_product[product_id][-5:],
        }

    def rename_category(self, category_id: str, new_name: str) -> int:
        category = self.categories_by_id.get(category_id)
        if category is None:
            return 0
        category["name"] = new_name
        category["slug"] = new_name.lower().replace(" ", "-")
        affected = 1
        for product in self.products_by_id.values():
            if category_id in product["category_ids"]:
                affected += 1
        return affected

    def analytical_query(self, limit: int) -> list[dict[str, Any]]:
        ratings_by_manufacturer: dict[str, list[int]] = defaultdict(list)
        for review in self.reviews_by_product.values():
            for item in review:
                product = self.products_by_id[item["product_id"]]
                ratings_by_manufacturer[product["manufacturer_id"]].append(item["rating"])
        rows = []
        for manufacturer_id, ratings in ratings_by_manufacturer.items():
            manufacturer = self.manufacturers_by_id[manufacturer_id]
            rows.append(
                {
                    "manufacturer_id": manufacturer_id,
                    "manufacturer_name": manufacturer["name"],
                    "review_count": len(ratings),
                    "avg_rating": sum(ratings) / len(ratings),
                }
            )
        return sorted(rows, key=lambda row: row["review_count"], reverse=True)[:limit]

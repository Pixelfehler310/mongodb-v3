from __future__ import annotations

from collections import defaultdict
from typing import Any

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.seed.generator import Catalog


class MongoAdapter(BenchmarkAdapter):
    database_type = "mongo"

    def __init__(self, uri: str, database_name: str, max_pool_size: int) -> None:
        self.uri = uri
        self.database_name = database_name
        self.max_pool_size = max_pool_size
        self.client: Any = None
        self.db: Any = None

    def connect(self) -> None:
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("pymongo is required for MongoDB benchmarks") from exc
        self.client = MongoClient(self.uri, maxPoolSize=self.max_pool_size, serverSelectionTimeoutMS=5000)
        self.client.admin.command("ping")
        self.db = self.client[self.database_name]

    def close(self) -> None:
        if self.client is not None:
            self.client.close()

    def reset(self) -> None:
        self.db.products.drop()
        self.db.categories.drop()
        self.db.manufacturers.drop()
        self.db.reviews.drop()

    def seed(self, catalog: Catalog) -> None:
        categories_by_id = {item["category_id"]: item for item in catalog.categories}
        variants_by_product: dict[str, list[dict[str, Any]]] = defaultdict(list)
        reviews_by_product: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for variant in catalog.variants:
            variants_by_product[variant["product_id"]].append(variant)
        for review in catalog.reviews:
            reviews_by_product[review["product_id"]].append(review)

        products = []
        for product in catalog.products:
            category_snapshots = [
                {
                    "category_id": category_id,
                    "name": categories_by_id[category_id]["name"],
                    "slug": categories_by_id[category_id]["slug"],
                }
                for category_id in product["category_ids"]
            ]
            products.append(
                {
                    **product,
                    "category_snapshots": category_snapshots,
                    "variants": variants_by_product[product["product_id"]],
                    "recent_reviews": reviews_by_product[product["product_id"]][-5:],
                }
            )

        if catalog.manufacturers:
            self.db.manufacturers.insert_many(catalog.manufacturers)
        if catalog.categories:
            self.db.categories.insert_many(catalog.categories)
        if products:
            self.db.products.insert_many(products)
        if catalog.reviews:
            self.db.reviews.insert_many(catalog.reviews)
        self._create_indexes()

    def _create_indexes(self) -> None:
        self.db.products.create_index("product_id", unique=True)
        self.db.products.create_index("manufacturer_id")
        self.db.products.create_index("category_ids")
        self.db.products.create_index("category_snapshots.category_id")
        self.db.categories.create_index("category_id", unique=True)
        self.db.manufacturers.create_index("manufacturer_id", unique=True)
        self.db.reviews.create_index("product_id")

    def validate(self, expected_counts: dict[str, int]) -> list[str]:
        actual = {
            "products": self.db.products.count_documents({}),
            "variants": sum(len(item.get("variants", [])) for item in self.db.products.find({}, {"variants": 1})),
            "reviews": self.db.reviews.count_documents({}),
            "categories": self.db.categories.count_documents({}),
            "manufacturers": self.db.manufacturers.count_documents({}),
        }
        messages = [f"{key}: expected {value}, got {actual[key]}" for key, value in expected_counts.items() if actual[key] != value]
        for collection, index_name in [("products", "product_id_1"), ("reviews", "product_id_1"), ("categories", "category_id_1")]:
            if index_name not in self.db[collection].index_information():
                messages.append(f"missing index {collection}.{index_name}")
        return messages

    def sample_product_ids(self, limit: int) -> list[str]:
        return [item["product_id"] for item in self.db.products.find({}, {"product_id": 1}).limit(limit)]

    def sample_category_ids(self, limit: int) -> list[str]:
        return [item["category_id"] for item in self.db.categories.find({}, {"category_id": 1}).limit(limit)]

    def read_product_aggregate(self, product_id: str) -> dict[str, Any] | None:
        product = self.db.products.find_one({"product_id": product_id}, {"_id": 0})
        if product is None:
            return None
        manufacturer = self.db.manufacturers.find_one({"manufacturer_id": product["manufacturer_id"]}, {"_id": 0})
        return {**product, "manufacturer": manufacturer}

    def rename_category(self, category_id: str, new_name: str) -> int:
        slug = new_name.lower().replace(" ", "-")
        category_result = self.db.categories.update_one({"category_id": category_id}, {"$set": {"name": new_name, "slug": slug}})
        product_result = self.db.products.update_many(
            {"category_snapshots.category_id": category_id},
            {"$set": {"category_snapshots.$[category].name": new_name, "category_snapshots.$[category].slug": slug}},
            array_filters=[{"category.category_id": category_id}],
        )
        return int(category_result.modified_count + product_result.modified_count)

    def analytical_query(self, limit: int) -> list[dict[str, Any]]:
        pipeline = [
            {"$group": {"_id": "$product_id", "avg_rating": {"$avg": "$rating"}, "review_count": {"$sum": 1}}},
            {"$lookup": {"from": "products", "localField": "_id", "foreignField": "product_id", "as": "product"}},
            {"$unwind": "$product"},
            {"$group": {"_id": "$product.manufacturer_id", "avg_rating": {"$avg": "$avg_rating"}, "review_count": {"$sum": "$review_count"}}},
            {"$lookup": {"from": "manufacturers", "localField": "_id", "foreignField": "manufacturer_id", "as": "manufacturer"}},
            {"$unwind": "$manufacturer"},
            {"$project": {"_id": 0, "manufacturer_id": "$_id", "manufacturer_name": "$manufacturer.name", "avg_rating": 1, "review_count": 1}},
            {"$sort": {"review_count": -1}},
            {"$limit": limit},
        ]
        return list(self.db.reviews.aggregate(pipeline))

    def explain_summary(self, scenario_id: str) -> dict[str, Any]:
        return {"scenario_id": scenario_id, "available": True, "engine": "mongodb", "note": "Use collection explain() for detailed local analysis."}

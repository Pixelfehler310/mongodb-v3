from __future__ import annotations

from typing import Any

from pymongo.errors import DuplicateKeyError

from .facets import build_facets
from . import mongo_format
from .product_contract import ProductConflictError, normalize_product_payload
from .query_logic import build_aggregation_pipeline
from .sample_data import build_live_sample


class MongoProductRepository:
    engine = "mongo"
    label = "MongoDB"
    query_language = "MongoDB query"
    code_language = "PyMongo"

    def __init__(self, database: Any):
        self.database = database
        self.collection = database.collection

    def ping(self) -> bool:
        return self.database.ping()

    def health_metadata(self) -> dict[str, Any]:
        hello = self.database.client.admin.command("hello")
        return {
            "database": self.database.settings.mongo_db,
            "collection": self.database.settings.mongo_collection,
            "model": "embedded product document",
            "replicaSet": hello.get("setName"),
            "primary": hello.get("primary"),
            "server": hello.get("me"),
            "isWritablePrimary": bool(hello.get("isWritablePrimary")),
            "writeConcern": self.database.settings.mongo_write_concern,
            "readConcern": self.database.settings.mongo_read_concern,
            "readPreference": self.database.settings.mongo_read_preference,
        }

    def facets(self) -> dict[str, Any]:
        return build_facets(self.collection)

    def list_products(self, product_query: Any) -> dict[str, Any]:
        cursor = self.collection.find(product_query.query).sort(list(product_query.sort.items())).limit(product_query.limit)
        items = list(cursor)
        total = self.collection.count_documents(product_query.query)
        return {
            "items": items,
            "total": total,
            "limit": product_query.limit,
            "activeFilters": product_query.filters,
            "queryText": mongo_format.format_find_query(product_query.query, product_query.sort, product_query.limit),
            "codeText": mongo_format.format_find_code(product_query.query, product_query.sort, product_query.limit),
        }

    def get_product_response(self, product_id: str) -> dict[str, Any] | None:
        item = self.collection.find_one({"_id": product_id}) or self.collection.find_one({"productId": product_id})
        if item is None:
            return None
        return {
            "item": item,
            "queryText": mongo_format.format_detail_query(product_id),
            "codeText": mongo_format.format_detail_code(product_id),
            "storageSummary": "One product document already contains categories, variants, reviews, attributes, and schema-version fields.",
        }

    def aggregation_response(self, kind: str) -> dict[str, Any]:
        pipeline = build_aggregation_pipeline(kind)
        return {
            "results": list(self.collection.aggregate(pipeline)),
            "queryText": mongo_format.format_aggregation_query(pipeline),
            "codeText": mongo_format.format_aggregation_code(pipeline),
        }

    def insert_sample_response(self, product_type: str) -> dict[str, Any]:
        sequence = self.collection.count_documents({"source": "live-sample"}) + 1
        document = build_live_sample(product_type=product_type, sequence=sequence)
        self.collection.insert_one(document)
        return {
            "item": document,
            "queryText": mongo_format.format_insert_query(document["_id"]),
            "codeText": mongo_format.format_insert_code(document["_id"]),
            "message": f"Inserted {document['name']} into MongoDB",
        }

    def create_product_response(self, payload: Any) -> dict[str, Any]:
        document = normalize_product_payload(payload)
        try:
            self.collection.insert_one(document)
        except DuplicateKeyError as error:
            raise ProductConflictError(f"Product {document['_id']} already exists.") from error
        return {
            "item": document,
            "queryText": mongo_format.format_insert_query(document["_id"]),
            "codeText": mongo_format.format_insert_code(document["_id"]),
            "message": f"Created {document['name']} in MongoDB",
        }

    def replace_product_response(self, product_id: str, payload: Any) -> dict[str, Any] | None:
        existing = self.collection.find_one({"_id": product_id}) or self.collection.find_one({"productId": product_id})
        if existing is None:
            return None
        document = normalize_product_payload(payload, existing=existing)
        self.collection.replace_one({"_id": existing["_id"]}, document)
        detail = self.get_product_response(existing["_id"])
        if detail is None:
            return None
        return {
            **detail,
            "message": f"Updated {document['name']} in MongoDB",
        }

    def delete_product_response(self, product_id: str) -> dict[str, Any] | None:
        existing = self.collection.find_one({"_id": product_id}) or self.collection.find_one({"productId": product_id})
        if existing is None:
            return None
        result = self.collection.delete_one({"_id": existing["_id"]})
        return {
            "productId": existing["_id"],
            "deletedCount": int(result.deleted_count),
            "message": f"Deleted {existing['name']} from MongoDB",
            "queryText": f"db.products.deleteOne({{ _id: {existing['_id']!r} }})",
            "codeText": f"collection.delete_one({{'_id': {existing['_id']!r}}})",
        }

    def category_rename_response(self, category_slug: str, new_name: str) -> dict[str, Any]:
        before = self.collection.count_documents({"categories.slug": category_slug})
        result = self.collection.update_many(
            {"categories.slug": category_slug},
            {"$set": {"categories.$[category].name": new_name}},
            array_filters=[{"category.slug": category_slug}],
        )
        return {
            "scenario": "category-rename",
            "engine": self.engine,
            "headline": "Denormalized snapshots must be updated inside every affected product document.",
            "categorySlug": category_slug,
            "newName": new_name,
            "beforeAffectedProducts": before,
            "changedProductDocuments": int(result.modified_count),
            "changedCategoryRows": 0,
            "queryText": mongo_format.format_category_rename_query(category_slug, new_name),
            "codeText": mongo_format.format_category_rename_code(category_slug, new_name),
        }

    def lazy_migration_response(self, product_type: str, tax_code: str) -> dict[str, Any]:
        selector = {"productType": product_type, "regionalTaxCode": {"$exists": False}}
        before = self.collection.count_documents(selector)
        result = self.collection.update_many(selector, {"$set": {"schemaVersion": 2, "regionalTaxCode": tax_code}})
        after = self.collection.count_documents(selector)
        return {
            "scenario": "lazy-migration",
            "engine": self.engine,
            "headline": "MongoDB can migrate only the touched legacy documents and keep old and new shapes valid during the transition.",
            "productType": product_type,
            "taxCode": tax_code,
            "legacyDocumentsBefore": before,
            "changedDocuments": int(result.modified_count),
            "legacyDocumentsAfter": after,
            "queryText": mongo_format.format_lazy_migration_query(product_type, tax_code),
            "codeText": mongo_format.format_lazy_migration_code(product_type, tax_code),
        }

    def product_count(self) -> int:
        return self.collection.count_documents({})
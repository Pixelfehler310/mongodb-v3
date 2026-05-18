from __future__ import annotations

from flask import Flask, jsonify, request
from pymongo.errors import PyMongoError
from werkzeug.exceptions import HTTPException

from .database import create_database
from .product_contract import ProductConflictError, ProductValidationError
from .query_logic import aggregation_label, build_product_query
from .repository import create_repository
from .serialization import serialize
from .settings import Settings


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask(__name__, static_folder=None)
    database = create_database(settings)
    repository = create_repository(database, settings.db_engine)

    @app.get("/")
    def index():
        return jsonify({"name": "Product Catalog Demo API", "engine": repository.engine, "ok": True})

    @app.get("/api/health")
    def health():
        repository.ping()
        return jsonify(
            {
                "ok": True,
                "engine": repository.engine,
                "label": repository.label,
                "queryLanguage": repository.query_language,
                "codeLanguage": repository.code_language,
                "productCount": repository.product_count(),
                **repository.health_metadata(),
            }
        )

    @app.get("/api/facets")
    def facets():
        return jsonify(serialize(repository.facets()))

    @app.get("/api/products")
    def products():
        product_query = build_product_query(request.args, settings.default_limit)
        return jsonify(serialize(repository.list_products(product_query)))

    @app.get("/api/products/<product_id>")
    def product_detail(product_id: str):
        response = repository.get_product_response(product_id)
        if response is None:
            return jsonify({"error": "Product not found", "productId": product_id}), 404
        return jsonify(serialize(response))

    @app.get("/api/aggregation")
    def aggregation():
        kind = request.args.get("kind", "avgPriceByType")
        response = repository.aggregation_response(kind)
        return jsonify(
            serialize(
                {
                    "kind": kind,
                    "label": aggregation_label(kind),
                    **response,
                }
            )
        )

    @app.post("/api/products/sample")
    def insert_sample():
        payload = request.get_json(silent=True) or {}
        product_type = payload.get("productType") or request.args.get("productType") or "laptop"
        return jsonify(serialize(repository.insert_sample_response(product_type))), 201

    @app.post("/api/products")
    def create_product():
        payload = request.get_json(silent=True)
        response = repository.create_product_response(payload)
        return jsonify(serialize(response)), 201

    @app.put("/api/products/<product_id>")
    def replace_product(product_id: str):
        payload = request.get_json(silent=True)
        response = repository.replace_product_response(product_id, payload)
        if response is None:
            return jsonify({"error": "Product not found", "productId": product_id}), 404
        return jsonify(serialize(response))

    @app.delete("/api/products/<product_id>")
    def delete_product(product_id: str):
        response = repository.delete_product_response(product_id)
        if response is None:
            return jsonify({"error": "Product not found", "productId": product_id}), 404
        return jsonify(serialize(response))

    @app.get("/api/demo/scenarios")
    def demo_scenarios():
        return jsonify(
            {
                "scenarios": [
                    {
                        "id": "document-shape",
                        "title": "Document vs. Main Entity",
                        "summary": "Compare a MongoDB product document with the PostgreSQL rows that hydrate the same API object.",
                    },
                    {
                        "id": "category-rename",
                        "title": "Denormalized Category Rename",
                        "summary": "Rename one category and compare embedded snapshot updates with a central relational update.",
                    },
                    {
                        "id": "lazy-migration",
                        "title": "Lazy Schema Evolution",
                        "summary": "Add regionalTaxCode to only the legacy documents or rows touched by the demo scenario.",
                    },
                    {
                        "id": "analytics",
                        "title": "Cross-Entity Analytics",
                        "summary": "Compare grouping from embedded reviews with joins over normalized review rows.",
                    },
                ]
            }
        )

    @app.post("/api/demo/scenarios/category-rename")
    def category_rename():
        payload = request.get_json(silent=True) or {}
        category_slug = payload.get("categorySlug") or request.args.get("categorySlug") or "work-essentials"
        new_name = payload.get("newName") or request.args.get("newName") or "Work Essentials Live"
        return jsonify(serialize(repository.category_rename_response(category_slug, new_name)))

    @app.post("/api/demo/scenarios/lazy-migration")
    def lazy_migration():
        payload = request.get_json(silent=True) or {}
        product_type = payload.get("productType") or request.args.get("productType") or "laptop"
        tax_code = payload.get("taxCode") or request.args.get("taxCode") or "DE-STD"
        return jsonify(serialize(repository.lazy_migration_response(product_type, tax_code)))

    @app.errorhandler(PyMongoError)
    def mongo_error(error: PyMongoError):
        return jsonify({"error": "MongoDB request failed", "detail": str(error)}), 503

    @app.errorhandler(ProductValidationError)
    def validation_error(error: ProductValidationError):
        return jsonify({"error": "Invalid product payload", "details": error.errors}), 400

    @app.errorhandler(ProductConflictError)
    def conflict_error(error: ProductConflictError):
        return jsonify({"error": "Product conflict", "detail": str(error)}), 409

    @app.errorhandler(Exception)
    def unexpected_error(error: Exception):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.name, "detail": error.description}), error.code or 500
        return jsonify({"error": "Unexpected server error", "detail": str(error)}), 500

    return app


if __name__ == "__main__":
    app_settings = Settings.from_env()
    create_app(app_settings).run(host="0.0.0.0", port=app_settings.port, debug=False)
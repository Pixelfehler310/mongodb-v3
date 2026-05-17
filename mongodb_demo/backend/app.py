from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from pymongo.errors import PyMongoError
from werkzeug.exceptions import HTTPException

from .database import MongoDatabase
from .facets import build_facets
from .mongo_format import (
    format_aggregation_code,
    format_aggregation_query,
    format_detail_code,
    format_detail_query,
    format_find_code,
    format_find_query,
    format_insert_code,
    format_insert_query,
)
from .query_logic import aggregation_label, build_aggregation_pipeline, build_product_query
from .repository import ProductRepository
from .serialization import serialize
from .settings import Settings


PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask(__name__, static_folder=str(PUBLIC_DIR), static_url_path="")
    database = MongoDatabase(settings)
    repository = ProductRepository(database.collection)

    @app.get("/")
    def index():
        return send_from_directory(PUBLIC_DIR, "index.html")

    @app.get("/api/health")
    def health():
        database.ping()
        return jsonify(
            {
                "ok": True,
                "database": settings.mongo_db,
                "collection": settings.mongo_collection,
                "productCount": repository.product_count(),
            }
        )

    @app.get("/api/facets")
    def facets():
        return jsonify(serialize(build_facets(database.collection)))

    @app.get("/api/products")
    def products():
        product_query = build_product_query(request.args, settings.default_limit)
        items, total = repository.list_products(product_query.query, product_query.sort, product_query.limit)
        return jsonify(
            serialize(
                {
                    "items": items,
                    "total": total,
                    "limit": product_query.limit,
                    "activeFilters": product_query.filters,
                    "queryText": format_find_query(product_query.query, product_query.sort, product_query.limit),
                    "codeText": format_find_code(product_query.query, product_query.sort, product_query.limit),
                }
            )
        )

    @app.get("/api/products/<product_id>")
    def product_detail(product_id: str):
        item = repository.get_product(product_id)
        if item is None:
            return jsonify({"error": "Product not found", "productId": product_id}), 404
        return jsonify(
            serialize(
                {
                    "item": item,
                    "queryText": format_detail_query(product_id),
                    "codeText": format_detail_code(product_id),
                }
            )
        )

    @app.get("/api/aggregation")
    def aggregation():
        kind = request.args.get("kind", "avgPriceByType")
        pipeline = build_aggregation_pipeline(kind)
        return jsonify(
            serialize(
                {
                    "kind": kind,
                    "label": aggregation_label(kind),
                    "results": repository.aggregate(kind),
                    "queryText": format_aggregation_query(pipeline),
                    "codeText": format_aggregation_code(pipeline),
                }
            )
        )

    @app.post("/api/products/sample")
    def insert_sample():
        payload = request.get_json(silent=True) or {}
        product_type = payload.get("productType") or request.args.get("productType") or "laptop"
        item = repository.insert_sample_product(product_type)
        return jsonify(
            serialize(
                {
                    "item": item,
                    "queryText": format_insert_query(item["_id"]),
                    "codeText": format_insert_code(item["_id"]),
                    "message": f"Inserted {item['name']}",
                }
            )
        ), 201

    @app.errorhandler(PyMongoError)
    def mongo_error(error: PyMongoError):
        return jsonify({"error": "MongoDB request failed", "detail": str(error)}), 503

    @app.errorhandler(Exception)
    def unexpected_error(error: Exception):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.name, "detail": error.description}), error.code or 500
        return jsonify({"error": "Unexpected server error", "detail": str(error)}), 500

    return app


if __name__ == "__main__":
    app_settings = Settings.from_env()
    create_app(app_settings).run(host="0.0.0.0", port=app_settings.port, debug=True)
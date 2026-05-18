from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from . import postgres_format
from .postgres_schema import insert_postgres_product
from .product_contract import ProductConflictError, normalize_product_payload
from .query_logic import AGGREGATIONS
from .sample_data import PRODUCT_TYPES, STATUSES, build_live_sample


class PostgresProductRepository:
    engine = "postgres"
    label = "PostgreSQL"
    query_language = "SQL query"
    code_language = "psycopg"

    def __init__(self, database: Any):
        self.database = database
        self.connection: Any = database.connection

    def ping(self) -> bool:
        return self.database.ping()

    def health_metadata(self) -> dict[str, Any]:
        return {"database": "product_demo", "schema": "public", "model": "normalized relational tables"}

    def product_count(self) -> int:
        row = self.connection.execute("SELECT COUNT(*) AS count FROM products").fetchone()
        return int(row["count"])

    def facets(self) -> dict[str, Any]:
        return {
            "productTypes": self._column_values("SELECT DISTINCT product_type AS value FROM products ORDER BY value") or PRODUCT_TYPES,
            "manufacturers": self._column_values("SELECT DISTINCT name AS value FROM manufacturers ORDER BY value"),
            "categories": self.connection.execute("SELECT slug, name FROM categories ORDER BY name").fetchall(),
            "statuses": self._column_values("SELECT DISTINCT status AS value FROM products ORDER BY value") or STATUSES,
            "ramOptions": [
                int(value)
                for value in self._column_values(
                    "SELECT DISTINCT value_num AS value FROM product_attributes WHERE attr_key = 'ramGb' ORDER BY value"
                )
                if value is not None
            ],
            "schemaEvolution": [
                {"value": "withTaxCode", "label": "with regionalTaxCode"},
                {"value": "withoutTaxCode", "label": "without regionalTaxCode"},
            ],
            "aggregations": [{"kind": key, "label": value} for key, value in AGGREGATIONS.items()],
        }

    def list_products(self, product_query: Any) -> dict[str, Any]:
        sql, params = self._build_list_sql(product_query.filters, product_query.limit)
        count_sql, count_params = self._build_count_sql(product_query.filters)
        rows = self.connection.execute(sql, params).fetchall()
        count_row = self.connection.execute(count_sql, count_params).fetchone()
        items = self._hydrate_products([row["id"] for row in rows])
        return {
            "items": items,
            "total": int(count_row["count"]),
            "limit": product_query.limit,
            "activeFilters": product_query.filters,
            "queryText": postgres_format.format_sql_query(sql, params),
            "codeText": postgres_format.format_sql_code(sql, params),
        }

    def get_product_response(self, product_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT id FROM products WHERE id = %s OR product_id = %s",
            [product_id, product_id],
        ).fetchone()
        if row is None:
            return None
        item = self._hydrate_product(row["id"])
        return {
            "item": item,
            "queryText": postgres_format.format_detail_query(product_id),
            "codeText": postgres_format.format_detail_code(product_id),
            "storageSummary": "The API object is hydrated from products, manufacturers, categories, attributes, variants, highlights, and reviews.",
        }

    def aggregation_response(self, kind: str) -> dict[str, Any]:
        sql = self._aggregation_sql(kind)
        rows = self.connection.execute(sql).fetchall()
        return {
            "results": [dict(row) for row in rows],
            "queryText": postgres_format.format_sql_query(sql, []),
            "codeText": postgres_format.format_sql_code(sql, []),
        }

    def insert_sample_response(self, product_type: str) -> dict[str, Any]:
        sequence_row = self.connection.execute("SELECT COUNT(*) AS count FROM products WHERE source = 'live-sample'").fetchone()
        document = build_live_sample(product_type=product_type, sequence=int(sequence_row["count"]) + 1)
        insert_postgres_product(self.connection, document)
        return {
            "item": self._hydrate_product(document["_id"]),
            "queryText": postgres_format.format_insert_query(document["_id"]),
            "codeText": postgres_format.format_insert_code(document["_id"]),
            "message": f"Inserted {document['name']} into PostgreSQL",
        }

    def create_product_response(self, payload: Any) -> dict[str, Any]:
        document = normalize_product_payload(payload)
        existing_row = self.connection.execute(
            "SELECT id FROM products WHERE id = %s OR product_id = %s",
            [document["_id"], document["productId"]],
        ).fetchone()
        if existing_row is not None:
            raise ProductConflictError(f"Product {document['_id']} already exists.")
        with self.connection.transaction():
            insert_postgres_product(self.connection, document)
        return {
            "item": self._hydrate_product(document["_id"]),
            "queryText": postgres_format.format_insert_query(document["_id"]),
            "codeText": postgres_format.format_insert_code(document["_id"]),
            "message": f"Created {document['name']} in PostgreSQL",
        }

    def replace_product_response(self, product_id: str, payload: Any) -> dict[str, Any] | None:
        existing = self.get_product_response(product_id)
        if existing is None:
            return None
        document = normalize_product_payload(payload, existing=existing["item"])
        with self.connection.transaction():
            insert_postgres_product(self.connection, document)
        detail = self.get_product_response(document["_id"])
        if detail is None:
            return None
        return {
            **detail,
            "message": f"Updated {document['name']} in PostgreSQL",
        }

    def delete_product_response(self, product_id: str) -> dict[str, Any] | None:
        existing = self.get_product_response(product_id)
        if existing is None:
            return None
        product = existing["item"]
        with self.connection.transaction():
            for table_name in ["product_reviews", "product_highlights", "product_variants", "product_attributes", "product_categories"]:
                self.connection.execute(f"DELETE FROM {table_name} WHERE product_id = %s", [product["_id"]])
            result = self.connection.execute("DELETE FROM products WHERE id = %s", [product["_id"]])
        return {
            "productId": product["_id"],
            "deletedCount": int(result.rowcount),
            "message": f"Deleted {product['name']} from PostgreSQL",
            "queryText": postgres_format.format_sql_query("DELETE FROM products WHERE id = %s", [product["_id"]]),
            "codeText": "connection.execute('DELETE FROM products WHERE id = %s', [product_id])",
        }

    def category_rename_response(self, category_slug: str, new_name: str) -> dict[str, Any]:
        count_row = self.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM product_categories pc
            JOIN categories c ON c.id = pc.category_id
            WHERE c.slug = %s
            """,
            [category_slug],
        ).fetchone()
        result = self.connection.execute("UPDATE categories SET name = %s WHERE slug = %s", [new_name, category_slug])
        return {
            "scenario": "category-rename",
            "engine": self.engine,
            "headline": "Only the central category row changes; related products keep pointing to the same category id.",
            "categorySlug": category_slug,
            "newName": new_name,
            "beforeAffectedProducts": int(count_row["count"]),
            "changedProductDocuments": 0,
            "changedCategoryRows": int(result.rowcount),
            "queryText": postgres_format.format_category_rename_query(category_slug, new_name),
            "codeText": postgres_format.format_category_rename_code(category_slug, new_name),
        }

    def lazy_migration_response(self, product_type: str, tax_code: str) -> dict[str, Any]:
        before_row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM products WHERE product_type = %s AND regional_tax_code IS NULL",
            [product_type],
        ).fetchone()
        result = self.connection.execute(
            "UPDATE products SET schema_version = 2, regional_tax_code = %s WHERE product_type = %s AND regional_tax_code IS NULL",
            [tax_code, product_type],
        )
        after_row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM products WHERE product_type = %s AND regional_tax_code IS NULL",
            [product_type],
        ).fetchone()
        return {
            "scenario": "lazy-migration",
            "engine": self.engine,
            "headline": "PostgreSQL makes the evolution explicit in the products table and updates rows through one controlled statement.",
            "productType": product_type,
            "taxCode": tax_code,
            "legacyDocumentsBefore": int(before_row["count"]),
            "changedDocuments": int(result.rowcount),
            "legacyDocumentsAfter": int(after_row["count"]),
            "queryText": postgres_format.format_lazy_migration_query(product_type, tax_code),
            "codeText": postgres_format.format_lazy_migration_code(product_type, tax_code),
        }

    def _column_values(self, sql: str) -> list[Any]:
        return [row["value"] for row in self.connection.execute(sql).fetchall()]

    def _build_list_sql(self, filters: dict[str, Any], limit: int) -> tuple[str, list[Any]]:
        where_sql, params = self._build_where(filters)
        sql = """
            SELECT p.id
            FROM products p
            JOIN manufacturers m ON m.id = p.manufacturer_id
            {where_sql}
            ORDER BY p.updated_at DESC
            LIMIT %s
        """.format(where_sql=where_sql)
        return sql, [*params, limit]

    def _build_count_sql(self, filters: dict[str, Any]) -> tuple[str, list[Any]]:
        where_sql, params = self._build_where(filters)
        sql = """
            SELECT COUNT(*) AS count
            FROM products p
            JOIN manufacturers m ON m.id = p.manufacturer_id
            {where_sql}
        """.format(where_sql=where_sql)
        return sql, params

    def _build_where(self, filters: dict[str, Any]) -> tuple[str, list[Any]]:
        clauses: list[str] = []
        params: list[Any] = []
        exact_columns = {
            "productType": "p.product_type",
            "manufacturer": "m.name",
            "status": "p.status",
        }
        for filter_name, column_name in exact_columns.items():
            if filters.get(filter_name):
                clauses.append(f"{column_name} = %s")
                params.append(filters[filter_name])

        if filters.get("category"):
            clauses.append(
                """
                EXISTS (
                    SELECT 1 FROM product_categories pc
                    JOIN categories c ON c.id = pc.category_id
                    WHERE pc.product_id = p.id AND c.slug = %s
                )
                """
            )
            params.append(filters["category"])
        if filters.get("minPrice") is not None:
            clauses.append("p.base_price >= %s")
            params.append(filters["minPrice"])
        if filters.get("maxPrice") is not None:
            clauses.append("p.base_price <= %s")
            params.append(filters["maxPrice"])
        if filters.get("ramMin") is not None:
            clauses.append(
                """
                EXISTS (
                    SELECT 1 FROM product_attributes pa
                    WHERE pa.product_id = p.id AND pa.attr_key = 'ramGb' AND pa.value_num >= %s
                )
                """
            )
            params.append(filters["ramMin"])
        if filters.get("schemaEvolution") == "withTaxCode":
            clauses.append("p.regional_tax_code IS NOT NULL")
        elif filters.get("schemaEvolution") == "withoutTaxCode":
            clauses.append("p.regional_tax_code IS NULL")
        if filters.get("search"):
            clauses.append(
                """
                (p.name ILIKE %s OR EXISTS (
                    SELECT 1 FROM product_highlights ph
                    WHERE ph.product_id = p.id AND ph.highlight ILIKE %s
                ))
                """
            )
            pattern = f"%{filters['search']}%"
            params.extend([pattern, pattern])

        if not clauses:
            return "", []
        return "WHERE " + " AND ".join(clauses), params

    def _aggregation_sql(self, kind: str) -> str:
        if kind == "avgRatingByManufacturer":
            return """
                SELECT m.name AS _id, AVG(pr.rating)::float AS "averageRating", COUNT(*)::int AS "reviewCount"
                FROM products p
                JOIN manufacturers m ON m.id = p.manufacturer_id
                JOIN product_reviews pr ON pr.product_id = p.id
                GROUP BY m.name
                ORDER BY "averageRating" DESC, _id ASC
            """
        return """
            SELECT p.product_type AS _id, AVG(p.base_price)::float AS "averagePrice", COUNT(*)::int AS count
            FROM products p
            GROUP BY p.product_type
            ORDER BY _id ASC
        """

    def _hydrate_products(self, product_ids: list[str]) -> list[dict[str, Any]]:
        return [self._hydrate_product(product_id) for product_id in product_ids]

    def _hydrate_product(self, product_id: str) -> dict[str, Any]:
        row = self.connection.execute(
            """
            SELECT p.*, m.name AS manufacturer_name
            FROM products p
            JOIN manufacturers m ON m.id = p.manufacturer_id
            WHERE p.id = %s
            """,
            [product_id],
        ).fetchone()
        categories = self.connection.execute(
            """
            SELECT c.id, c.name, c.slug
            FROM product_categories pc
            JOIN categories c ON c.id = pc.category_id
            WHERE pc.product_id = %s
            ORDER BY pc.position ASC
            """,
            [product_id],
        ).fetchall()
        document: dict[str, Any] = {
            "_id": row["id"],
            "productId": row["product_id"],
            "sku": row["sku"],
            "productType": row["product_type"],
            "name": row["name"],
            "basePrice": _number(row["base_price"]),
            "currency": row["currency"],
            "manufacturer": {"id": row["manufacturer_id"], "name": row["manufacturer_name"]},
            "categories": [dict(category) for category in categories],
            "attributes": self._load_attributes(product_id),
            "variants": self.connection.execute(
                "SELECT variant_id AS \"variantId\", label, inventory_count AS \"inventoryCount\" FROM product_variants WHERE product_id = %s ORDER BY position ASC",
                [product_id],
            ).fetchall(),
            "highlights": self._column_values_for_product("product_highlights", "highlight", product_id),
            "latestReviews": self.connection.execute(
                "SELECT review_id AS \"reviewId\", rating, title FROM product_reviews WHERE product_id = %s ORDER BY position ASC",
                [product_id],
            ).fetchall(),
            "status": row["status"],
            "schemaVersion": row["schema_version"],
            "createdAt": _iso(row["created_at"]),
            "updatedAt": _iso(row["updated_at"]),
        }
        if row["regional_tax_code"] is not None:
            document["regionalTaxCode"] = row["regional_tax_code"]
        if row["source"] is not None:
            document["source"] = row["source"]
        return document

    def _load_attributes(self, product_id: str) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        rows = self.connection.execute(
            "SELECT attr_key, value_text, value_num, value_bool FROM product_attributes WHERE product_id = %s ORDER BY attr_key ASC",
            [product_id],
        ).fetchall()
        for row in rows:
            if row["value_bool"] is not None:
                value = row["value_bool"]
            elif row["value_num"] is not None:
                value = _number(row["value_num"])
            else:
                value = row["value_text"]
            attributes[row["attr_key"]] = value
        return attributes

    def _column_values_for_product(self, table_name: str, column_name: str, product_id: str) -> list[Any]:
        rows = self.connection.execute(
            f"SELECT {column_name} AS value FROM {table_name} WHERE product_id = %s ORDER BY position ASC",
            [product_id],
        ).fetchall()
        return [row["value"] for row in rows]


def _iso(value: Any) -> str:
    if isinstance(value, datetime):
        return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return str(value)


def _number(value: Any) -> int | float:
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value
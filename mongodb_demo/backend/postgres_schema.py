from __future__ import annotations

from datetime import datetime
from typing import Any


def recreate_postgres_schema(connection: Any) -> None:
    statements = [
        "DROP TABLE IF EXISTS product_reviews, product_highlights, product_variants, product_attributes, product_categories, products, categories, manufacturers CASCADE",
        "CREATE TABLE manufacturers (id text PRIMARY KEY, name text NOT NULL)",
        "CREATE TABLE categories (id text PRIMARY KEY, name text NOT NULL, slug text NOT NULL UNIQUE)",
        """
        CREATE TABLE products (
            id text PRIMARY KEY,
            product_id text NOT NULL UNIQUE,
            sku text NOT NULL,
            product_type text NOT NULL,
            name text NOT NULL,
            base_price numeric(12, 2) NOT NULL,
            currency text NOT NULL,
            manufacturer_id text NOT NULL REFERENCES manufacturers(id),
            status text NOT NULL,
            schema_version integer NOT NULL,
            regional_tax_code text NULL,
            source text NULL,
            created_at timestamptz NOT NULL,
            updated_at timestamptz NOT NULL
        )
        """,
        "CREATE TABLE product_categories (product_id text REFERENCES products(id), category_id text REFERENCES categories(id), position integer NOT NULL, PRIMARY KEY (product_id, category_id))",
        "CREATE TABLE product_attributes (product_id text REFERENCES products(id), attr_key text NOT NULL, value_text text NULL, value_num double precision NULL, value_bool boolean NULL, PRIMARY KEY (product_id, attr_key))",
        "CREATE TABLE product_variants (product_id text REFERENCES products(id), variant_id text NOT NULL, label text NOT NULL, inventory_count integer NOT NULL, position integer NOT NULL, PRIMARY KEY (product_id, variant_id))",
        "CREATE TABLE product_highlights (product_id text REFERENCES products(id), highlight text NOT NULL, position integer NOT NULL, PRIMARY KEY (product_id, position))",
        "CREATE TABLE product_reviews (product_id text REFERENCES products(id), review_id text NOT NULL, rating integer NOT NULL, title text NOT NULL, position integer NOT NULL, PRIMARY KEY (product_id, review_id))",
        "CREATE INDEX idx_products_type ON products(product_type)",
        "CREATE INDEX idx_products_updated_at ON products(updated_at DESC)",
        "CREATE INDEX idx_products_regional_tax_code ON products(regional_tax_code)",
        "CREATE INDEX idx_product_attributes_key_num ON product_attributes(attr_key, value_num)",
    ]
    with connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)


def seed_postgres_products(connection: Any, products: list[dict[str, Any]]) -> None:
    for product in products:
        insert_postgres_product(connection, product)


def insert_postgres_product(connection: Any, product: dict[str, Any]) -> None:
    manufacturer = product["manufacturer"]
    connection.execute(
        "INSERT INTO manufacturers (id, name) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
        [manufacturer["id"], manufacturer["name"]],
    )
    for category in product["categories"]:
        connection.execute(
            "INSERT INTO categories (id, name, slug) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, slug = EXCLUDED.slug",
            [category["id"], category["name"], category["slug"]],
        )
    connection.execute(
        """
        INSERT INTO products (
            id, product_id, sku, product_type, name, base_price, currency, manufacturer_id,
            status, schema_version, regional_tax_code, source, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            sku = EXCLUDED.sku,
            name = EXCLUDED.name,
            base_price = EXCLUDED.base_price,
            status = EXCLUDED.status,
            regional_tax_code = EXCLUDED.regional_tax_code,
            source = EXCLUDED.source,
            updated_at = EXCLUDED.updated_at
        """,
        [
            product["_id"],
            product["productId"],
            product["sku"],
            product["productType"],
            product["name"],
            product["basePrice"],
            product["currency"],
            manufacturer["id"],
            product["status"],
            product["schemaVersion"],
            product.get("regionalTaxCode"),
            product.get("source"),
            _parse_iso(product["createdAt"]),
            _parse_iso(product["updatedAt"]),
        ],
    )
    _insert_child_rows(connection, product)


def _insert_child_rows(connection: Any, product: dict[str, Any]) -> None:
    product_id = product["_id"]
    for table_name in ["product_categories", "product_attributes", "product_variants", "product_highlights", "product_reviews"]:
        connection.execute(f"DELETE FROM {table_name} WHERE product_id = %s", [product_id])
    for position, category in enumerate(product["categories"]):
        connection.execute(
            "INSERT INTO product_categories (product_id, category_id, position) VALUES (%s, %s, %s)",
            [product_id, category["id"], position],
        )
    for attr_key, value in product["attributes"].items():
        value_text, value_num, value_bool = _split_attribute_value(value)
        connection.execute(
            "INSERT INTO product_attributes (product_id, attr_key, value_text, value_num, value_bool) VALUES (%s, %s, %s, %s, %s)",
            [product_id, attr_key, value_text, value_num, value_bool],
        )
    for position, variant in enumerate(product["variants"]):
        connection.execute(
            "INSERT INTO product_variants (product_id, variant_id, label, inventory_count, position) VALUES (%s, %s, %s, %s, %s)",
            [product_id, variant["variantId"], variant["label"], variant["inventoryCount"], position],
        )
    for position, highlight in enumerate(product["highlights"]):
        connection.execute(
            "INSERT INTO product_highlights (product_id, highlight, position) VALUES (%s, %s, %s)",
            [product_id, highlight, position],
        )
    for position, review in enumerate(product["latestReviews"]):
        connection.execute(
            "INSERT INTO product_reviews (product_id, review_id, rating, title, position) VALUES (%s, %s, %s, %s, %s)",
            [product_id, review["reviewId"], review["rating"], review["title"], position],
        )


def _split_attribute_value(value: Any) -> tuple[str | None, float | None, bool | None]:
    if isinstance(value, bool):
        return None, None, value
    if isinstance(value, (int, float)):
        return None, float(value), None
    return str(value), None, None


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
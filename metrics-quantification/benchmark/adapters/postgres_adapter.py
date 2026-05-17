from __future__ import annotations

from typing import Any

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.seed.generator import Catalog


class PostgresAdapter(BenchmarkAdapter):
    database_type = "postgres"

    def __init__(self, dsn: str, pool_min: int, pool_max: int) -> None:
        self.dsn = dsn
        self.pool_min = pool_min
        self.pool_max = pool_max
        self.pool: Any = None

    def connect(self) -> None:
        try:
            from psycopg2.pool import ThreadedConnectionPool
        except ImportError as exc:
            raise RuntimeError("psycopg2-binary is required for PostgreSQL benchmarks") from exc
        self.pool = ThreadedConnectionPool(self.pool_min, self.pool_max, dsn=self.dsn)

    def close(self) -> None:
        if self.pool is not None:
            self.pool.closeall()

    def _connection(self):
        connection = self.pool.getconn()
        try:
            yield connection
        finally:
            self.pool.putconn(connection)

    def reset(self) -> None:
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DROP TABLE IF EXISTS reviews, variants, product_categories, laptop_details,
                    tshirt_details, book_details, smartphone_details, desk_details, products,
                    categories, manufacturers CASCADE;
                    """
                )
                connection.commit()
                self._create_schema(cursor)
                connection.commit()

    def _create_schema(self, cursor: Any) -> None:
        cursor.execute(
            """
            CREATE TABLE manufacturers (
                manufacturer_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            );
            CREATE TABLE categories (
                category_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                parent_category_id TEXT NULL
            );
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                sku TEXT NOT NULL,
                product_type TEXT NOT NULL,
                name TEXT NOT NULL,
                base_price NUMERIC NOT NULL,
                currency TEXT NOT NULL,
                manufacturer_id TEXT NOT NULL REFERENCES manufacturers(manufacturer_id),
                status TEXT NOT NULL,
                regional_tax_code TEXT NULL,
                created_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL
            );
            CREATE TABLE product_categories (
                product_id TEXT NOT NULL REFERENCES products(product_id),
                category_id TEXT NOT NULL REFERENCES categories(category_id),
                PRIMARY KEY (product_id, category_id)
            );
            CREATE TABLE variants (
                variant_id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL REFERENCES products(product_id),
                label TEXT NOT NULL,
                price_delta NUMERIC NOT NULL,
                inventory_count INTEGER NOT NULL,
                color TEXT NULL,
                size_label TEXT NULL
            );
            CREATE TABLE reviews (
                review_id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL REFERENCES products(product_id),
                user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL,
                verified_purchase BOOLEAN NOT NULL
            );
            CREATE TABLE laptop_details (product_id TEXT PRIMARY KEY REFERENCES products(product_id), cpu_model TEXT, ram_gb INTEGER, storage_gb INTEGER, gpu_model TEXT, screen_size_inches NUMERIC);
            CREATE TABLE tshirt_details (product_id TEXT PRIMARY KEY REFERENCES products(product_id), size TEXT, material TEXT, fit TEXT, color TEXT, target_group TEXT);
            CREATE TABLE book_details (product_id TEXT PRIMARY KEY REFERENCES products(product_id), author TEXT, isbn TEXT, page_count INTEGER, language TEXT, publisher TEXT);
            CREATE TABLE smartphone_details (product_id TEXT PRIMARY KEY REFERENCES products(product_id), soc TEXT, display_inches NUMERIC, battery_mah INTEGER, camera_mp INTEGER, os_family TEXT);
            CREATE TABLE desk_details (product_id TEXT PRIMARY KEY REFERENCES products(product_id), material TEXT, width_cm INTEGER, height_cm INTEGER, depth_cm INTEGER, max_load_kg INTEGER);
            CREATE INDEX idx_products_manufacturer ON products(manufacturer_id);
            CREATE INDEX idx_product_categories_category ON product_categories(category_id);
            CREATE INDEX idx_variants_product ON variants(product_id);
            CREATE INDEX idx_reviews_product ON reviews(product_id);
            """
        )

    def seed(self, catalog: Catalog) -> None:
        try:
            from psycopg2.extras import execute_values
        except ImportError as exc:
            raise RuntimeError("psycopg2-binary is required for PostgreSQL benchmarks") from exc

        with self._pooled() as connection:
            with connection.cursor() as cursor:
                execute_values(cursor, "INSERT INTO manufacturers (manufacturer_id, name, country) VALUES %s", [(item["manufacturer_id"], item["name"], item["country"]) for item in catalog.manufacturers])
                execute_values(cursor, "INSERT INTO categories (category_id, name, slug, parent_category_id) VALUES %s", [(item["category_id"], item["name"], item["slug"], item["parent_category_id"]) for item in catalog.categories])
                execute_values(
                    cursor,
                    """
                    INSERT INTO products (product_id, sku, product_type, name, base_price, currency, manufacturer_id, status, regional_tax_code, created_at, updated_at)
                    VALUES %s
                    """,
                    [
                        (
                            item["product_id"], item["sku"], item["product_type"], item["name"], item["base_price"], item["currency"],
                            item["manufacturer_id"], item["status"], item.get("regional_tax_code"), item["created_at"], item["updated_at"],
                        )
                        for item in catalog.products
                    ],
                )
                execute_values(cursor, "INSERT INTO product_categories (product_id, category_id) VALUES %s", [(item["product_id"], category_id) for item in catalog.products for category_id in item["category_ids"]])
                execute_values(cursor, "INSERT INTO variants (variant_id, product_id, label, price_delta, inventory_count, color, size_label) VALUES %s", [(item["variant_id"], item["product_id"], item["label"], item["price_delta"], item["inventory_count"], item["variant_attributes"].get("color"), item["variant_attributes"].get("size")) for item in catalog.variants])
                execute_values(cursor, "INSERT INTO reviews (review_id, product_id, user_id, rating, title, text, created_at, verified_purchase) VALUES %s", [(item["review_id"], item["product_id"], item["user_id"], item["rating"], item["title"], item["text"], item["created_at"], item["verified_purchase"]) for item in catalog.reviews])
                self._seed_detail_tables(cursor, execute_values, catalog)
                connection.commit()

    def _seed_detail_tables(self, cursor: Any, execute_values: Any, catalog: Catalog) -> None:
        rows: dict[str, list[tuple[Any, ...]]] = {"laptop": [], "tshirt": [], "book": [], "smartphone": [], "desk": []}
        for item in catalog.products:
            attrs = item["type_attributes"]
            if item["product_type"] == "laptop":
                rows["laptop"].append((item["product_id"], attrs["cpu_model"], attrs["ram_gb"], attrs["storage_gb"], attrs["gpu_model"], attrs["screen_size_inches"]))
            elif item["product_type"] == "tshirt":
                rows["tshirt"].append((item["product_id"], attrs["size"], attrs["material"], attrs["fit"], attrs["color"], attrs["target_group"]))
            elif item["product_type"] == "book":
                rows["book"].append((item["product_id"], attrs["author"], attrs["isbn"], attrs["page_count"], attrs["language"], attrs["publisher"]))
            elif item["product_type"] == "smartphone":
                rows["smartphone"].append((item["product_id"], attrs["soc"], attrs["display_inches"], attrs["battery_mah"], attrs["camera_mp"], attrs["os_family"]))
            elif item["product_type"] == "desk":
                rows["desk"].append((item["product_id"], attrs["material"], attrs["width_cm"], attrs["height_cm"], attrs["depth_cm"], attrs["max_load_kg"]))
        statements = {
            "laptop": "INSERT INTO laptop_details (product_id, cpu_model, ram_gb, storage_gb, gpu_model, screen_size_inches) VALUES %s",
            "tshirt": "INSERT INTO tshirt_details (product_id, size, material, fit, color, target_group) VALUES %s",
            "book": "INSERT INTO book_details (product_id, author, isbn, page_count, language, publisher) VALUES %s",
            "smartphone": "INSERT INTO smartphone_details (product_id, soc, display_inches, battery_mah, camera_mp, os_family) VALUES %s",
            "desk": "INSERT INTO desk_details (product_id, material, width_cm, height_cm, depth_cm, max_load_kg) VALUES %s",
        }
        for key, values in rows.items():
            if values:
                execute_values(cursor, statements[key], values)

    def validate(self, expected_counts: dict[str, int]) -> list[str]:
        tables = {"products": "products", "variants": "variants", "reviews": "reviews", "categories": "categories", "manufacturers": "manufacturers"}
        messages: list[str] = []
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                for key, table_name in tables.items():
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    actual = cursor.fetchone()[0]
                    if actual != expected_counts[key]:
                        messages.append(f"{key}: expected {expected_counts[key]}, got {actual}")
        return messages

    def sample_product_ids(self, limit: int) -> list[str]:
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT product_id FROM products ORDER BY product_id LIMIT %s", (limit,))
                return [row[0] for row in cursor.fetchall()]

    def sample_category_ids(self, limit: int) -> list[str]:
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT category_id FROM categories ORDER BY category_id LIMIT %s", (limit,))
                return [row[0] for row in cursor.fetchall()]

    def read_product_aggregate(self, product_id: str) -> dict[str, Any] | None:
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT p.product_id, p.sku, p.product_type, p.name, p.base_price, p.currency, p.manufacturer_id, m.name
                    FROM products p JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
                    WHERE p.product_id = %s
                    """,
                    (product_id,),
                )
                product = cursor.fetchone()
                if product is None:
                    return None
                cursor.execute("SELECT variant_id, label, price_delta, inventory_count FROM variants WHERE product_id = %s ORDER BY variant_id", (product_id,))
                variants = cursor.fetchall()
                cursor.execute("SELECT c.category_id, c.name, c.slug FROM categories c JOIN product_categories pc ON pc.category_id = c.category_id WHERE pc.product_id = %s ORDER BY c.category_id", (product_id,))
                categories = cursor.fetchall()
                cursor.execute("SELECT review_id, rating, title, created_at FROM reviews WHERE product_id = %s ORDER BY created_at DESC LIMIT 5", (product_id,))
                reviews = cursor.fetchall()
        return {
            "product_id": product[0],
            "sku": product[1],
            "product_type": product[2],
            "name": product[3],
            "base_price": float(product[4]),
            "currency": product[5],
            "manufacturer": {"manufacturer_id": product[6], "name": product[7]},
            "variants": [{"variant_id": row[0], "label": row[1], "price_delta": float(row[2]), "inventory_count": row[3]} for row in variants],
            "categories": [{"category_id": row[0], "name": row[1], "slug": row[2]} for row in categories],
            "recent_reviews": [{"review_id": row[0], "rating": row[1], "title": row[2], "created_at": row[3].isoformat()} for row in reviews],
        }

    def rename_category(self, category_id: str, new_name: str) -> int:
        slug = new_name.lower().replace(" ", "-")
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE categories SET name = %s, slug = %s WHERE category_id = %s", (new_name, slug, category_id))
                affected = cursor.rowcount
                connection.commit()
        return affected

    def analytical_query(self, limit: int) -> list[dict[str, Any]]:
        with self._pooled() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.manufacturer_id, m.name, COUNT(r.review_id) AS review_count, AVG(r.rating)::float AS avg_rating
                    FROM manufacturers m
                    JOIN products p ON p.manufacturer_id = m.manufacturer_id
                    JOIN reviews r ON r.product_id = p.product_id
                    GROUP BY m.manufacturer_id, m.name
                    ORDER BY review_count DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cursor.fetchall()
        return [{"manufacturer_id": row[0], "manufacturer_name": row[1], "review_count": row[2], "avg_rating": row[3]} for row in rows]

    def explain_summary(self, scenario_id: str) -> dict[str, Any]:
        return {"scenario_id": scenario_id, "available": True, "engine": "postgresql", "note": "Use EXPLAIN ANALYZE for detailed local analysis."}

    from contextlib import contextmanager

    @contextmanager
    def _pooled(self):
        connection = self.pool.getconn()
        try:
            yield connection
        finally:
            self.pool.putconn(connection)

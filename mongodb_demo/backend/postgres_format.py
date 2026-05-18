from __future__ import annotations

from typing import Any, Sequence


DETAIL_LOOKUP_SQL = "SELECT id FROM products WHERE id = %s OR product_id = %s"


def _format_params(params: Sequence[Any]) -> str:
    if not params:
        return "[]"
    return "[" + ", ".join(repr(item) for item in params) + "]"


def format_sql_query(sql: str, params: Sequence[Any]) -> str:
    return sql.strip() + "\n\n-- params: " + _format_params(params)


def format_sql_code(sql: str, params: Sequence[Any]) -> str:
    return (
        "sql = "
        + repr(sql.strip())
        + "\nparams = "
        + _format_params(params)
        + "\n\nwith psycopg.connect(dsn, row_factory=dict_row) as conn:\n"
        + "    rows = conn.execute(sql, params).fetchall()"
    )


def format_detail_query(product_id: str) -> str:
    return format_sql_query(DETAIL_LOOKUP_SQL, [product_id, product_id])


def format_detail_code(product_id: str) -> str:
    return (
        "sql = "
        + repr(DETAIL_LOOKUP_SQL)
        + "\nparams = "
        + _format_params([product_id, product_id])
        + "\n\nwith psycopg.connect(dsn, row_factory=dict_row) as conn:\n"
        + "    row = conn.execute(sql, params).fetchone()"
    )


def format_insert_query(product_id: str) -> str:
    return format_sql_query("INSERT INTO products (id, product_id, ...) VALUES (%s, %s, ...)", [product_id, product_id])


def format_insert_code(product_id: str) -> str:
    return "insert_product(conn, build_sample_product(product_id=" + repr(product_id) + "))"


def format_category_rename_query(category_slug: str, new_name: str) -> str:
    return format_sql_query("UPDATE categories SET name = %s WHERE slug = %s", [new_name, category_slug])


def format_category_rename_code(category_slug: str, new_name: str) -> str:
    return (
        "sql = 'UPDATE categories SET name = %s WHERE slug = %s'\n"
        + "params = "
        + _format_params([new_name, category_slug])
        + "\n\nconn.execute(sql, params)"
    )


def format_lazy_migration_query(product_type: str, tax_code: str) -> str:
    return format_sql_query(
        "UPDATE products SET schema_version = 2, regional_tax_code = %s WHERE product_type = %s AND regional_tax_code IS NULL",
        [tax_code, product_type],
    )


def format_lazy_migration_code(product_type: str, tax_code: str) -> str:
    return (
        "sql = 'UPDATE products SET schema_version = 2, regional_tax_code = %s WHERE product_type = %s AND regional_tax_code IS NULL'\n"
        + "params = "
        + _format_params([tax_code, product_type])
        + "\n\nconn.execute(sql, params)"
    )
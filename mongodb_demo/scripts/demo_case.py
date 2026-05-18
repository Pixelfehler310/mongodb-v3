from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BACKEND_URLS = {
    "mongo": "http://localhost:5000",
    "postgres": "http://localhost:5001",
}


def request_json(base_url: str, path: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        base_url.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def print_heading(title: str) -> None:
    print("\n" + title)
    print("=" * len(title))


def print_kv(payload: dict, keys: list[str]) -> None:
    width = max(len(key) for key in keys)
    for key in keys:
        if key in payload:
            print(f"{key:<{width}} : {payload[key]}")


def run_command(args: argparse.Namespace) -> None:
    base_url = args.url or BACKEND_URLS[args.backend]
    if args.command == "health":
        payload = request_json(base_url, "/api/health")
        print_heading(f"{payload['label']} health")
        print_kv(payload, ["ok", "engine", "model", "productCount", "database"])
        return

    if args.command == "read-aggregate":
        products = request_json(base_url, "/api/products?limit=1")
        first = products["items"][0]
        detail = request_json(base_url, f"/api/products/{first['_id']}")
        print_heading(f"{args.backend} product aggregate")
        print_kv(detail["item"], ["_id", "productType", "name", "schemaVersion", "regionalTaxCode"])
        print("\nQuery:\n" + detail["queryText"])
        return

    if args.command == "category-rename":
        payload = request_json(
            base_url,
            "/api/demo/scenarios/category-rename",
            {"categorySlug": args.category_slug, "newName": args.new_name},
        )
        print_heading(f"{args.backend} category rename")
        print(payload["headline"])
        print_kv(payload, ["beforeAffectedProducts", "changedCategoryRows", "changedProductDocuments"])
        print("\nQuery:\n" + payload["queryText"])
        return

    if args.command == "lazy-migration":
        payload = request_json(
            base_url,
            "/api/demo/scenarios/lazy-migration",
            {"productType": args.product_type, "taxCode": args.tax_code},
        )
        print_heading(f"{args.backend} lazy migration")
        print(payload["headline"])
        print_kv(payload, ["legacyDocumentsBefore", "changedDocuments", "legacyDocumentsAfter"])
        print("\nQuery:\n" + payload["queryText"])
        return

    aggregation = request_json(base_url, f"/api/aggregation?kind={args.kind}")
    print_heading(f"{args.backend} aggregation: {aggregation['label']}")
    for row in aggregation["results"]:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print("\nQuery:\n" + aggregation["queryText"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run presentation demo scenarios against a local backend API.")
    parser.add_argument("--backend", choices=BACKEND_URLS, default="mongo")
    parser.add_argument("--url", help="Override backend base URL, for example http://localhost:5000")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health")
    subparsers.add_parser("read-aggregate")

    rename = subparsers.add_parser("category-rename")
    rename.add_argument("--category-slug", default="work-essentials")
    rename.add_argument("--new-name", default="Work Essentials Live")

    migrate = subparsers.add_parser("lazy-migration")
    migrate.add_argument("--product-type", default="laptop")
    migrate.add_argument("--tax-code", default="DE-STD")

    aggregation = subparsers.add_parser("aggregation")
    aggregation.add_argument("--kind", default="avgPriceByType")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_command(args)
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Demo request failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
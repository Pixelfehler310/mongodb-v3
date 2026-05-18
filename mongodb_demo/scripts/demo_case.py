from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BACKEND_URLS = {
    "mongo": "http://localhost:5000",
    "postgres": "http://localhost:5001",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_SERVICES = ("mongo1", "mongo2")


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


def run_compose(*args: str) -> None:
    subprocess.run(["docker", "compose", *args], cwd=PROJECT_ROOT, check=True)


def wait_for_primary(
    base_url: str, previous_primary: str | None = None, timeout_seconds: int = 25
) -> dict:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            payload = request_json(base_url, "/api/health")
            primary = str(payload.get("primary") or "")
            if primary and (previous_primary is None or primary != previous_primary):
                return payload
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
        time.sleep(1)
    if last_error is not None:
        raise last_error
    raise TimeoutError("Timed out waiting for a writable primary")


def pick_product(base_url: str, product_id: str | None = None) -> dict:
    if product_id:
        detail = request_json(base_url, f"/api/products/{product_id}")
        return detail["item"]
    products = request_json(base_url, "/api/products?limit=1")
    if not products.get("items"):
        raise RuntimeError("No demo products available")
    return products["items"][0]


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
        print_kv(
            detail["item"],
            ["_id", "productType", "name", "schemaVersion", "regionalTaxCode"],
        )
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
        print_kv(
            payload,
            [
                "beforeAffectedProducts",
                "changedCategoryRows",
                "changedProductDocuments",
            ],
        )
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
        print_kv(
            payload,
            ["legacyDocumentsBefore", "changedDocuments", "legacyDocumentsAfter"],
        )
        print("\nQuery:\n" + payload["queryText"])
        return

    if args.command == "risky-failover":
        health = request_json(base_url, "/api/health")
        if health.get("engine") != "mongo":
            raise RuntimeError(
                "The risky failover demo only works against the MongoDB backend"
            )

        primary = str(health.get("primary") or "")
        primary_service = primary.split(":", 1)[0]
        if primary_service not in DATA_SERVICES:
            raise RuntimeError(
                f"Unexpected primary returned by health endpoint: {primary or 'missing'}"
            )
        secondary_service = next(
            service for service in DATA_SERVICES if service != primary_service
        )

        product = pick_product(base_url, args.product_id)
        risky_name = args.new_name or f"{product['name']} [w=1-demo {int(time.time())}]"

        print_heading("MongoDB risky failover demo")
        print_kv(
            {
                "primary": primary_service,
                "secondary": secondary_service,
                "product": product["_id"],
                "writeConcern": health.get("writeConcern"),
            },
            ["primary", "secondary", "product", "writeConcern"],
        )

        secondary_paused = False
        primary_stopped = False
        try:
            print(
                f"\n1) Pause secondary {secondary_service} so it cannot replicate the next write."
            )
            run_compose("pause", secondary_service)
            secondary_paused = True

            print("2) Trigger risky w=1 update.")
            result = request_json(
                base_url,
                f"/api/demo/risky-update/{product['_id']}",
                {"name": risky_name},
            )
            print_kv(
                result, ["status", "matched_count", "modified_count", "latency_ms"]
            )

            print(f"\n3) Stop primary {primary_service} after the acknowledged write.")
            run_compose("stop", primary_service)
            primary_stopped = True

            print(f"4) Resume secondary {secondary_service} so election can finish.")
            run_compose("unpause", secondary_service)
            secondary_paused = False

            new_health = wait_for_primary(
                base_url,
                previous_primary=primary,
                timeout_seconds=args.election_timeout,
            )
            current = request_json(base_url, f"/api/products/{product['_id']}")
            persisted = current["item"].get("name") == risky_name

            print(f"\n5) New primary: {new_health.get('primary')}")
            print(f"   Observed product name: {current['item'].get('name')}")
            print(f"   Risky name written   : {risky_name}")
            print("\nOutcome:")
            if persisted:
                print(
                    "The write survived this run. Retry if replication won the race before failover."
                )
            else:
                print(
                    "The acknowledged w=1 write disappeared after failover. This is the controlled rollback/loss path."
                )
        finally:
            if secondary_paused:
                run_compose("unpause", secondary_service)
            if primary_stopped and not args.leave_primary_down:
                print(
                    f"\n6) Restart {primary_service} to restore the original topology."
                )
                run_compose("start", primary_service)
        return

    aggregation = request_json(base_url, f"/api/aggregation?kind={args.kind}")
    print_heading(f"{args.backend} aggregation: {aggregation['label']}")
    for row in aggregation["results"]:
        print(" | ".join(f"{key}={value}" for key, value in row.items()))
    print("\nQuery:\n" + aggregation["queryText"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run presentation demo scenarios against a local backend API."
    )
    parser.add_argument("--backend", choices=BACKEND_URLS, default="mongo")
    parser.add_argument(
        "--url", help="Override backend base URL, for example http://localhost:5000"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health")
    subparsers.add_parser("read-aggregate")

    rename = subparsers.add_parser("category-rename")
    rename.add_argument("--category-slug", default="work-essentials")
    rename.add_argument("--new-name", default="Work Essentials Live")

    migrate = subparsers.add_parser("lazy-migration")
    migrate.add_argument("--product-type", default="laptop")
    migrate.add_argument("--tax-code", default="DE-STD")

    risky = subparsers.add_parser("risky-failover")
    risky.add_argument("--product-id")
    risky.add_argument("--new-name")
    risky.add_argument("--election-timeout", type=int, default=25)
    risky.add_argument("--leave-primary-down", action="store_true")

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

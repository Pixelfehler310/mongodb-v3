from __future__ import annotations

from benchmark.adapters.base import BenchmarkAdapter


def expected_counts(profile_counts: dict[str, int]) -> dict[str, int]:
    return {
        "products": profile_counts["products"],
        "variants": profile_counts["variants"],
        "reviews": profile_counts["reviews"],
        "categories": profile_counts["categories"],
        "manufacturers": profile_counts["manufacturers"],
    }


def run_preflight(adapter: BenchmarkAdapter, profile_counts: dict[str, int]) -> list[str]:
    messages = adapter.validate(expected_counts(profile_counts))
    if not adapter.sample_product_ids(1):
        messages.append("no product sample available")
    if not adapter.sample_category_ids(1):
        messages.append("no category sample available")
    return messages

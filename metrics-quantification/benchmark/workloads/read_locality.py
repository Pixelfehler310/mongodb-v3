from __future__ import annotations

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.models import OperationResult
from benchmark.workloads.common import measure


def run_read_locality(adapter: BenchmarkAdapter, operations: int, warmup_label: str | None = None) -> list[OperationResult]:
    _ = warmup_label
    product_ids = adapter.sample_product_ids(max(operations, 1))
    results = []
    for index in range(operations):
        product_id = product_ids[index % len(product_ids)]
        results.append(measure("product_aggregate_read", lambda product_id=product_id: adapter.read_product_aggregate(product_id)))
    return results

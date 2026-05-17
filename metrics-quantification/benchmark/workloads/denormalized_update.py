from __future__ import annotations

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.models import OperationResult
from benchmark.workloads.common import measure


def run_denormalized_update(adapter: BenchmarkAdapter, operations: int, warmup_label: str | None = None) -> list[OperationResult]:
    category_ids = adapter.sample_category_ids(max(operations, 1))
    results = []
    for index in range(operations):
        category_id = category_ids[index % len(category_ids)]
        suffix = warmup_label or "measure"
        results.append(measure("category_rename", lambda category_id=category_id, index=index, suffix=suffix: adapter.rename_category(category_id, f"Category {suffix} {index:04d}")))
    return results

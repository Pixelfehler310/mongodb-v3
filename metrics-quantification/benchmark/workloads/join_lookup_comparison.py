from __future__ import annotations

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.models import OperationResult
from benchmark.workloads.common import measure


def run_join_lookup(adapter: BenchmarkAdapter, operations: int, warmup_label: str | None = None) -> list[OperationResult]:
    _ = warmup_label
    return [measure("analytical_join_lookup", lambda: adapter.analytical_query(limit=20)) for _index in range(operations)]

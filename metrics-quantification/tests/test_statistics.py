from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.models import OperationResult, WorkloadDefinition, WorkloadRun
from benchmark.statistics import percentile, summarize_workload


def test_percentile_interpolates_values():
    assert percentile([1.0, 2.0, 3.0, 4.0], 50) == 2.5
    assert percentile([10.0], 95) == 10.0
    assert percentile([], 95) == 0.0


def test_summarize_workload_exports_required_metrics():
    scenario = WorkloadDefinition("read-locality", "Read Locality", "aggregate-read", "tiny", 1, 3, True)
    workload_run = WorkloadRun.create("run-test", scenario, "mongo", "tiny", 0, 42, True, 3)
    workload_run.operation_results = [
        OperationResult("read", True, 1.0),
        OperationResult("read", True, 3.0),
        OperationResult("read", False, 2.0, "timeout", "timed out"),
    ]

    summary = summarize_workload(workload_run)

    assert summary["successful_operations"] == 2
    assert summary["failed_operations"] == 1
    assert summary["mean_latency_ms"] == 2.0
    assert summary["p50_latency_ms"] == 2.0
    assert summary["notes"] == "timeout=1"

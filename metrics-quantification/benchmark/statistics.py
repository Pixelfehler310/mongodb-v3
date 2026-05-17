from __future__ import annotations

import math
from statistics import mean, stdev

from benchmark.models import OperationResult, WorkloadRun


def percentile(values: list[float], percentile_value: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    rank = (len(sorted_values) - 1) * (percentile_value / 100.0)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return sorted_values[int(rank)]
    weight = rank - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def summarize_workload(workload_run: WorkloadRun) -> dict[str, float | int | str | bool | None]:
    successful = [result for result in workload_run.operation_results if result.success]
    failed = [result for result in workload_run.operation_results if not result.success]
    latencies = [result.latency_ms for result in successful]
    total_latency_ms = sum(result.latency_ms for result in workload_run.operation_results)
    throughput = (len(successful) / (total_latency_ms / 1000.0)) if total_latency_ms > 0 else 0.0
    stddev = stdev(latencies) if len(latencies) > 1 else 0.0
    ci95 = 1.96 * stddev / math.sqrt(len(latencies)) if latencies else 0.0
    return {
        "run_id": workload_run.run_id,
        "timestamp_utc": workload_run.timestamp_utc,
        "scenario_id": workload_run.scenario_id,
        "scenario_name": workload_run.scenario_name,
        "database_type": workload_run.database_type,
        "dataset_profile": workload_run.dataset_profile,
        "repetition_index": workload_run.repetition_index,
        "seed": workload_run.seed,
        "warmup_used": workload_run.warmup_used,
        "total_operations": workload_run.total_operations,
        "successful_operations": len(successful),
        "failed_operations": len(failed),
        "throughput_ops_per_sec": throughput,
        "mean_latency_ms": mean(latencies) if latencies else 0.0,
        "stddev_latency_ms": stddev,
        "ci95_latency_ms": ci95,
        "p50_latency_ms": percentile(latencies, 50),
        "p90_latency_ms": percentile(latencies, 90),
        "p95_latency_ms": percentile(latencies, 95),
        "p99_latency_ms": percentile(latencies, 99),
        "max_latency_ms": max(latencies) if latencies else 0.0,
        "notes": _error_notes(failed),
    }


def operation_result(operation: str, success: bool, latency_ms: float, error: Exception | None = None) -> OperationResult:
    return OperationResult(
        operation=operation,
        success=success,
        latency_ms=latency_ms,
        error_class=classify_error(error) if error else None,
        error_message=str(error) if error else None,
    )


def classify_error(error: Exception | None) -> str | None:
    if error is None:
        return None
    name = type(error).__name__.lower()
    message = str(error).lower()
    if "timeout" in name or "timeout" in message:
        return "timeout"
    if "connect" in name or "connection" in message:
        return "connection_error"
    if "validation" in name or "integrity" in name:
        return "data_integrity_error"
    if "query" in name or "syntax" in message:
        return "query_error"
    return "unknown_error"


def _error_notes(failed: list[OperationResult]) -> str | None:
    if not failed:
        return None
    counts: dict[str, int] = {}
    for result in failed:
        key = result.error_class or "unknown_error"
        counts[key] = counts.get(key, 0) + 1
    return ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))

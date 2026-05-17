from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from benchmark.models import OperationResult
from benchmark.statistics import operation_result


def measure(operation: str, action: Callable[[], Any]) -> OperationResult:
    start = time.perf_counter()
    try:
        action()
    except (RuntimeError, TimeoutError, LookupError, ValueError, OSError) as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        return operation_result(operation, False, latency_ms, exc)
    latency_ms = (time.perf_counter() - start) * 1000
    return operation_result(operation, True, latency_ms)

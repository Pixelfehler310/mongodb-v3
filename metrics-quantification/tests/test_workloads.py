from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.adapters.in_memory_adapter import InMemoryAdapter
from benchmark.seed.generator import DATASET_PROFILES, generate_catalog
from benchmark.workloads.denormalized_update import run_denormalized_update
from benchmark.workloads.join_lookup_comparison import run_join_lookup
from benchmark.workloads.read_locality import run_read_locality


def seeded_adapter() -> InMemoryAdapter:
    adapter = InMemoryAdapter("mongo")
    adapter.connect()
    adapter.seed(generate_catalog(DATASET_PROFILES["tiny"], seed=42))
    return adapter


def test_workloads_return_successful_operation_results():
    adapter = seeded_adapter()

    read_results = run_read_locality(adapter, 3)
    update_results = run_denormalized_update(adapter, 3)
    join_results = run_join_lookup(adapter, 3)

    assert all(result.success for result in read_results)
    assert all(result.success for result in update_results)
    assert all(result.success for result in join_results)
    assert len(read_results) == 3
    assert len(update_results) == 3
    assert len(join_results) == 3

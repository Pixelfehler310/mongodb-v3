from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.export import export_run


def test_export_run_writes_raw_and_processed_files(tmp_path):
    base_raw_dir = tmp_path / "exports" / "raw"
    paths = export_run(
        base_raw_dir=base_raw_dir,
        run_id="run-test",
        manifest={"run_id": "run-test"},
        raw_results=[{"scenario_id": "read-locality"}],
        summaries=[{"p95_latency_ms": 1.25}],
    )

    assert (paths["raw_dir"] / "manifest.json").exists()
    assert (paths["raw_dir"] / "raw_results.json").exists()
    assert (paths["raw_dir"] / "environment.json").exists()
    assert (paths["processed_dir"] / "summary.json").exists()
    assert json.loads((paths["processed_dir"] / "summary.json").read_text())[0]["p95_latency_ms"] == 1.25

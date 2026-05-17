from __future__ import annotations

import json
import platform
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=json_default), encoding="utf-8")


def export_run(base_raw_dir: Path, run_id: str, manifest: dict[str, Any], raw_results: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> dict[str, Path]:
    raw_dir = base_raw_dir / run_id
    processed_dir = base_raw_dir.parent / "processed" / run_id
    environment = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }
    write_json(raw_dir / "manifest.json", manifest)
    write_json(raw_dir / "raw_results.json", raw_results)
    write_json(raw_dir / "environment.json", environment)
    write_json(processed_dir / "summary.json", summaries)
    return {"raw_dir": raw_dir, "processed_dir": processed_dir}

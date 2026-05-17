from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.table import Table

from benchmark.adapters.base import BenchmarkAdapter
from benchmark.adapters.in_memory_adapter import InMemoryAdapter
from benchmark.adapters.mongo_adapter import MongoAdapter
from benchmark.adapters.postgres_adapter import PostgresAdapter
from benchmark.config import load_settings
from benchmark.export import export_run
from benchmark.fairness_checks import run_preflight
from benchmark.models import WorkloadRun
from benchmark.seed.generator import DATASET_PROFILES, generate_catalog
from benchmark.statistics import summarize_workload
from benchmark.workload_catalog import SCENARIOS, scenario_list
from benchmark.workloads.denormalized_update import run_denormalized_update
from benchmark.workloads.join_lookup_comparison import run_join_lookup
from benchmark.workloads.read_locality import run_read_locality

console = Console()


WORKLOAD_RUNNERS = {
    "read-locality": run_read_locality,
    "denormalized-update": run_denormalized_update,
    "join-lookup": run_join_lookup,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run product-catalog MongoDB/PostgreSQL benchmark scenarios.")
    parser.add_argument("--scenario", choices=[*SCENARIOS.keys(), "all"], default="all")
    parser.add_argument("--db", choices=["postgres", "mongo", "all"], default="all")
    parser.add_argument("--dataset", choices=DATASET_PROFILES.keys(), default=None)
    parser.add_argument("--repetitions", type=int, default=None)
    parser.add_argument("--operations", type=int, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--warmup", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--skip-seed", action="store_true")
    parser.add_argument("--seed-only", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Use deterministic in-memory adapters instead of real databases.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = load_settings()
    dataset_name = args.dataset or settings.default_dataset
    profile = DATASET_PROFILES[dataset_name]
    scenarios = scenario_list(args.scenario)
    databases = ["postgres", "mongo"] if args.db == "all" else [args.db]
    run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"

    catalog = generate_catalog(profile, seed=args.seed)
    adapters = build_adapters(args, settings, databases)
    raw_results: list[dict] = []
    summaries: list[dict] = []

    try:
        for adapter in adapters:
            console.print(f"[bold]Preparing {adapter.database_type}[/bold]")
            adapter.connect()
            if not args.skip_seed:
                adapter.reset()
                adapter.seed(catalog)

            validation_messages = run_preflight(adapter, profile.as_counts())
            if validation_messages:
                for message in validation_messages:
                    console.print(f"[red]{adapter.database_type}: {message}[/red]")
                return 2
            if args.seed_only or args.validate_only:
                continue

            for scenario in scenarios:
                operations = args.operations or scenario.default_operations
                repetitions = args.repetitions or scenario.default_repetitions
                if args.warmup:
                    WORKLOAD_RUNNERS[scenario.scenario_id](adapter, max(1, min(operations, 10)), warmup_label="warmup")
                for repetition_index in range(repetitions):
                    workload_run = WorkloadRun.create(
                        run_id=run_id,
                        scenario=scenario,
                        database_type=adapter.database_type,
                        dataset_profile=profile.name,
                        repetition_index=repetition_index,
                        seed=args.seed,
                        warmup_used=args.warmup,
                        total_operations=operations,
                    )
                    workload_run.operation_results = WORKLOAD_RUNNERS[scenario.scenario_id](adapter, operations)
                    raw_results.append(workload_run.__dict__)
                    summary = summarize_workload(workload_run)
                    if args.explain and scenario.supports_explain:
                        summary["explain_summary"] = adapter.explain_summary(scenario.scenario_id)
                    summaries.append(summary)
                    print_summary(summary)
    finally:
        for adapter in adapters:
            adapter.close()

    if args.export and not (args.seed_only or args.validate_only):
        output_dir = args.output_dir or settings.export_dir
        manifest = {
            "run_id": run_id,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "dataset_profile": profile.name,
            "seed": args.seed,
            "active_scenarios": [scenario.scenario_id for scenario in scenarios],
            "active_databases": databases,
            "warmup_enabled": args.warmup,
            "repetition_count": args.repetitions,
            "notes": "Generated by metrics-quantification benchmark runner.",
        }
        paths = export_run(output_dir, run_id, manifest, raw_results, summaries)
        console.print(f"[green]Exported raw results to {paths['raw_dir']}[/green]")
        console.print(f"[green]Exported processed summary to {paths['processed_dir']}[/green]")
    return 0


def build_adapters(args: argparse.Namespace, settings, databases: list[str]) -> list[BenchmarkAdapter]:
    if args.dry_run:
        return [InMemoryAdapter(database_type) for database_type in databases]
    adapters: list[BenchmarkAdapter] = []
    for database_type in databases:
        if database_type == "postgres":
            adapters.append(PostgresAdapter(settings.postgres_dsn, settings.postgres_pool_min, settings.postgres_pool_max))
        elif database_type == "mongo":
            adapters.append(MongoAdapter(settings.mongo_uri, settings.mongo_db, settings.mongo_max_pool_size))
    return adapters


def print_summary(summary: dict) -> None:
    table = Table(show_header=False, box=None)
    table.add_row("scenario", summary["scenario_id"])
    table.add_row("database", summary["database_type"])
    table.add_row("p95_ms", f"{summary['p95_latency_ms']:.3f}")
    table.add_row("throughput", f"{summary['throughput_ops_per_sec']:.2f} ops/s")
    table.add_row("errors", str(summary["failed_operations"]))
    console.print(table)


if __name__ == "__main__":
    sys.exit(main())

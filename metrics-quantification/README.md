# Metrics Quantification Project

This folder contains the quantitative benchmark and metrics project for the seminar work. It is deliberately separated from the future demo project: this project produces reproducible measurements and exports, while the demo project can focus on visual explanation.

## Scope

The project compares MongoDB and PostgreSQL for the shared polymorphic product-catalog domain described in the concept files.

Core scenarios:

- `read-locality`: complete product aggregate read with variants, categories, manufacturer, and recent reviews.
- `denormalized-update`: category rename where MongoDB may carry duplicated category snapshots.
- `join-lookup`: analytical query over products, manufacturers, and reviews.

Non-goals:

- no web frontend,
- no HTTP API,
- no presentation demo,
- no cluster-first benchmark narrative.

## Requirements

- Python 3.11+
- pnpm
- Docker with Docker Compose

## Quickstart

```bash
pnpm install
pnpm setup
pnpm test
pnpm smoke
```

`pnpm smoke` runs the benchmark runner against deterministic in-memory adapters. It is intended as a fast local correctness check and does not replace database benchmarks.

## Database Benchmark Flow

```bash
cp .env.example .env
pnpm docker:up
pnpm benchmark
pnpm docker:down
```

The default benchmark command runs all core scenarios for both databases with the small dataset profile. Results are written below `exports/`.

## Useful pnpm Scripts

- `pnpm setup`: install Python dependencies into the active Python environment.
- `pnpm test`: run unit tests.
- `pnpm smoke`: run a tiny in-memory benchmark and export results.
- `pnpm validate`: run database preflight validation.
- `pnpm seed`: reset and seed MongoDB and PostgreSQL.
- `pnpm benchmark`: run all benchmark scenarios against MongoDB and PostgreSQL.
- `pnpm benchmark:read`: run only the read-locality scenario.
- `pnpm benchmark:update`: run only the denormalized-update scenario.
- `pnpm benchmark:join`: run only the join-lookup scenario.
- `pnpm docker:up`: start MongoDB and PostgreSQL.
- `pnpm docker:down`: stop databases and remove volumes.
- `pnpm docker:test`: run tests in the project container.
- `pnpm docker:benchmark`: run the benchmark from the project container.

## Export Contract

Every exported run creates:

- `exports/raw/<run_id>/manifest.json`
- `exports/raw/<run_id>/raw_results.json`
- `exports/raw/<run_id>/environment.json`
- `exports/processed/<run_id>/summary.json`

The raw files are machine-readable and should remain unedited. Processed summaries are the intended source for tables and charts.

## Method Notes

The implementation follows these guardrails from the concept documents:

- one shared product-catalog seed for both databases,
- explicit adapter boundary for MongoDB and PostgreSQL,
- fair connection and pooling strategy,
- separate warmup and measured operations,
- repeatable run manifests,
- structured error classes in raw results,
- exportable latency and throughput metrics.

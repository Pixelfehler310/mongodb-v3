# Metrics and Methods

This document operationalizes the quantitative part of the product-catalog comparison.

## Measurement Unit

One exported repetition measures one scenario for one database adapter. A repetition contains multiple operations so latency percentiles and throughput are calculated from a controlled batch rather than from a single query.

## Core Metrics

- `p50_latency_ms`: median successful operation latency.
- `p90_latency_ms`: 90th percentile successful operation latency.
- `p95_latency_ms`: 95th percentile successful operation latency.
- `p99_latency_ms`: 99th percentile successful operation latency.
- `mean_latency_ms`: arithmetic mean of successful operation latency.
- `stddev_latency_ms`: sample standard deviation of successful operation latency.
- `ci95_latency_ms`: approximate 95 percent confidence interval around the mean.
- `throughput_ops_per_sec`: successful operations divided by measured operation time.
- `failed_operations`: number of failed operations in the repetition.
- `notes`: compact error class summary when failures occur.

## Scenario A: Read Locality

Operation: load a complete product aggregate.

MongoDB reads the product document with embedded variants, category snapshots, and recent reviews, plus the referenced manufacturer. PostgreSQL reconstructs the aggregate from normalized tables.

Primary metrics:

- p50, p95, p99 latency,
- throughput,
- error rate.

## Scenario B: Denormalized Update

Operation: rename a category.

MongoDB updates the category document and duplicated category snapshots inside products. PostgreSQL updates the normalized category row.

Primary metrics:

- total operation latency,
- affected record or document count,
- error rate.

## Scenario C: Join versus Lookup

Operation: aggregate review statistics by manufacturer.

MongoDB uses aggregation with `$lookup`. PostgreSQL uses joins and grouping over normalized tables.

Primary metrics:

- p50, p95, p99 latency,
- throughput,
- explain or plan notes where available,
- error rate.

## Warmup Policy

When `--warmup` is enabled, each scenario runs a small unexported warmup batch before measured repetitions. Warmup results are intentionally excluded from raw and processed exports.

## Dataset Profiles

- `tiny`: local smoke checks.
- `small`: local development benchmark profile from the concept specification.
- `large`: full benchmark target profile from the concept specification.

## Fairness Rules

- Both databases are seeded from the same deterministic catalog object.
- PostgreSQL uses a threaded connection pool instead of a global serialized cursor.
- MongoDB uses the driver connection pool through `MongoClient`.
- Preflight validation checks counts and sample availability before measurement.
- Scenario names describe fachlich equivalent operations, not implementation details.

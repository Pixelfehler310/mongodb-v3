# Demo Scope

## Goal

The demo supports a 15-minute presentation about practical trade-offs between MongoDB and PostgreSQL. It should make the core comparison understandable without requiring live infrastructure failure tests or a benchmark lecture.

## In Scope

- One curated product catalog domain.
- Two interchangeable backends: MongoDB and PostgreSQL.
- Same HTTP API and frontend workflow for both backends.
- Guided story steps: catalog, storage shape, schema evolution, update scenario, analytics.
- CLI scenarios that call the same backend API as the frontend.
- Deterministic seed data with a small number of understandable products.

## Out of Scope for the Live Demo

- MongoDB replica sets and PostgreSQL replicas.
- Live CAP/failover claims.
- Sharding demonstrations.
- Large benchmark runs.
- Many product families, many filter dimensions, or enterprise-style dashboard detail.

These topics can still be discussed in the written seminar paper or in a backup slide as limitations and future work.

## Scientific Framing

The demo is not a proof that one database is generally better. It is a controlled illustration of data-model consequences:

- MongoDB favors aggregate-local reads and flexible evolution when product variants differ strongly.
- PostgreSQL favors explicit structure, central updates, constraints, and predictable analytical joins.
- Both systems can model the domain; the interesting question is which trade-off is cheaper for a given workload.

## Fairness Rules

- Both backends use the same seed data.
- Both expose the same API response shape.
- Both are shown through the same frontend screens.
- Demo claims must be phrased as design trade-offs, not universal performance conclusions.
# Demo Scope

## Goal

The demo supports a presentation about practical trade-offs between MongoDB and PostgreSQL. It now has a CRUD-first shop route for the application surface, a separate database showcase route for modeling trade-offs, and a controlled MongoDB replica-set path for CAP/failover discussion.

## In Scope

- One curated product catalog domain.
- Two interchangeable backends: MongoDB and PostgreSQL.
- Same HTTP API and frontend workflow for both backends.
- Full product CRUD through a form-based detail dialog on `/shop`.
- A database showcase route with storage shape, schema evolution, update scenario, query/code, and analytics views.
- MongoDB replica set in Docker with visible primary metadata.
- Controlled MongoDB failover and weak-write rollback/loss showcase.
- CLI scenarios that call the same backend API as the frontend.
- Deterministic seed data with a small number of understandable products.

## Out of Scope for the Live Demo

- PostgreSQL replication and automatic PostgreSQL failover.
- Sharding demonstrations.
- Large benchmark runs.
- Many product families, many filter dimensions, or enterprise-style dashboard detail.

PostgreSQL remains the relational CRUD/modeling comparison backend in this project. A fully distributed PostgreSQL HA setup would be a separate extension.

## Scientific Framing

The demo is not a proof that one database is generally better. It is a controlled illustration of data-model and distributed-system consequences:

- MongoDB favors aggregate-local reads and flexible evolution when product variants differ strongly.
- PostgreSQL favors explicit structure, central updates, constraints, and predictable analytical joins.
- MongoDB replica sets can preserve availability through election, while consistency and durability depend on read/write concern.
- Both systems can model the domain; the interesting question is which trade-off is cheaper for a given workload.

## Fairness Rules

- Both backends use the same seed data.
- Both expose the same API response shape.
- Both are shown through the same frontend screens.
- CRUD operations must use the same product JSON contract.
- CAP claims must name the concrete configuration, especially `w=1` versus `majority` write concern.
- Demo claims must be phrased as design trade-offs, not universal performance conclusions.
# Project Boundaries

This project is the quantitative metrics and benchmark project.

It owns:

- deterministic seed generation,
- MongoDB and PostgreSQL benchmark adapters,
- workload execution,
- fairness and preflight checks,
- metric calculation,
- raw and processed exports,
- containerized database workflow.

It does not own:

- a visual demo frontend,
- a didactic MongoDB-only showcase,
- presentation UI state,
- HTTP endpoints,
- unrelated e-commerce product features.

The later demo project can use the same domain language, but it should not depend on benchmark internals.

# Demo Scope

## Purpose

This project is a presentation artifact. It explains MongoDB document modeling with a small product catalog and keeps the audience focused on visible documents, filters, queries, code, aggregations, and schema evolution.

## In Scope

- Product list from MongoDB.
- Polymorphic product documents in one collection.
- Filters for type, manufacturer, category, price, status, nested RAM, shipping region, tags, search, and `regionalTaxCode` presence.
- Full JSON document view.
- MongoDB query display.
- PyMongo code display.
- Aggregation view.
- Prepared live sample insert.
- Deterministic seed data.

## Out of Scope

- SQL comparison.
- Benchmarking or metrics.
- Authentication.
- CRUD administration.
- Production hardening.
- React, Vite, or a larger frontend architecture.

## Architecture

```text
Browser UI -> Flask API -> PyMongo Repository -> MongoDB
```

The default local runtime is Docker Compose: MongoDB is exposed on host port `27117`, while the Flask app container serves both the API and the static frontend on host port `3000`.

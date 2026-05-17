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
- React/Vite frontend for the presentation UI.

## Out of Scope

- SQL comparison.
- Benchmarking or metrics.
- Authentication.
- CRUD administration.
- Production hardening.
- A larger frontend architecture beyond the demo UI.

## Architecture

```text
Browser UI -> Flask API -> PyMongo Repository -> MongoDB
```

The default local runtime is Docker Compose: MongoDB is exposed on host port `27117`, the Flask API is exposed on host port `5000`, and the React frontend is exposed on host port `3000`.

# MongoDB vs PostgreSQL Demo

Presentation-first demo for a 15-minute seminar talk. The application compares MongoDB and PostgreSQL on the same product-catalog domain, through the same API contract and the same frontend workflow.

The demo is intentionally small: it uses a curated catalog with laptops, t-shirts, and books, then shows where the two data models feel different in reads, storage shape, schema evolution, category updates, and aggregations.

## What This Demo Shows

- Same domain, same endpoints, two persistence models.
- MongoDB as embedded product documents with local product context.
- PostgreSQL as normalized relational tables with explicit structure.
- Schema evolution through older products without `regionalTaxCode` and newer products with it.
- Update contrast through a category rename scenario.
- Analytics contrast through average price and average rating aggregations.

This demo does not try to prove CAP behavior, sharding, replica-set failover, or absolute performance. Those topics belong in the written work or an appendix, not in the short live presentation.

## Run With Docker

```powershell
docker compose up --build
```

Open the frontend at:

```text
http://localhost:5173
```

Backend endpoints:

```text
MongoDB API:     http://localhost:5000/api
PostgreSQL API: http://localhost:5001/api
```

## Local Development

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install frontend dependencies:

```powershell
npm --prefix frontend install
```

Run the React frontend:

```powershell
npm --prefix frontend run dev
```

Run a backend manually, for example MongoDB:

```powershell
set DB_ENGINE=mongo&& set PORT=5000&& python -m backend.app
```

Run PostgreSQL manually:

```powershell
set DB_ENGINE=postgres&& set PORT=5001&& python -m backend.app
```

## Presentation CLI

The CLI calls the same HTTP API as the frontend. Start the Docker stack first, then run:

```powershell
npm run demo:health:mongo
npm run demo:health:postgres
npm run demo:read:mongo
npm run demo:read:postgres
npm run demo:rename:mongo
npm run demo:rename:postgres
npm run demo:migrate:mongo
npm run demo:migrate:postgres
```

The rename and migration commands are state-changing. Use the seed scripts or restart the Docker stack when you want to return to the original data state.

## Tests

```powershell
python -m pytest
npm --prefix frontend run build
```

## Data Model

MongoDB stores one product as one aggregate document with embedded categories, attributes, variants, highlights, and latest reviews.

PostgreSQL stores the same product through normalized tables: `products`, `manufacturers`, `categories`, `product_categories`, `product_attributes`, `product_variants`, `product_highlights`, and `product_reviews`.

Both backends expose the same high-level product JSON to the frontend so the comparison remains about data-model trade-offs, not about different application features.
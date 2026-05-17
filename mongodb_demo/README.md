# MongoDB Product Catalog Demo

Small Flask/PyMongo demo for a seminar presentation about MongoDB document modeling. The app shows a polymorphic product catalog with filters, full JSON documents, matching MongoDB query text, matching PyMongo code, simple aggregations, and a small schema-evolution example.

This project is only the qualitative demo. The metric and quantification project stays separate.

## Quick Start

```powershell
cd mongodb_demo
docker compose up --build
```

Open `http://localhost:3000`.

This starts four containers:

- `mongodb-demo` for MongoDB, exposed on host port `27117`.
- `mongodb-demo-seed` for deterministic seed data.
- `mongodb-demo-backend` for the Flask API, exposed on host port `5000`.
- `mongodb-demo-frontend` for the React frontend, exposed on host port `3000`.

## Local Development Start

Use this path when you want the Flask API and React app running directly on the host:

```powershell
cd mongodb_demo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d mongodb
Copy-Item .env.example .env
python scripts/seed.py
python -m backend.app
```

In a second terminal:

```powershell
cd mongodb_demo
npm --prefix frontend install
npm --prefix frontend run dev
```

The host-side MongoDB URI is `mongodb://localhost:27117/`, the Flask API runs on `http://localhost:5000`, and the React app runs on `http://localhost:3000`.

## What It Shows

- One `products` collection with laptops, t-shirts, books, smartphones, and desks.
- Shared product fields plus type-specific `attributes`.
- Embedded arrays such as `categories`, `variants`, `highlights`, and `latestReviews`.
- Filters over simple fields, nested fields, arrays, price range, and schema evolution.
- Query and PyMongo snippets that update with the UI state.
- Aggregations for average price, product counts, and average ratings.
- A sample insert button that creates a new schema-version-2 product with `regionalTaxCode`.

## Local Commands

```powershell
docker compose up --build
docker compose down
docker compose up -d mongodb
python scripts/seed.py
python -m backend.app
npm --prefix frontend run dev
npm --prefix frontend run build
python -m pytest
```

Equivalent npm script aliases are available for convenience:

```powershell
npm run compose:up
npm run compose:down
npm run seed
npm run reset
npm run start
npm test
```

## API

- `GET /api/health`
- `GET /api/facets`
- `GET /api/products`
- `GET /api/products/<product_id>`
- `GET /api/aggregation?kind=avgPriceByType`
- `POST /api/products/sample`

## Configuration

See `.env.example` for the supported variables:

- `PORT`
- `MONGO_URI`
- `MONGO_DB`
- `MONGO_COLLECTION`
- `DEFAULT_LIMIT`
- `DEMO_SEED_PROFILE`
- `ENABLE_EVOLUTION_VIEW`

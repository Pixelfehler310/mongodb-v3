# MongoDB vs PostgreSQL Demo

Presentation-first demo for a seminar talk. The application compares MongoDB and PostgreSQL on the same product-catalog domain, through the same API contract and a shared frontend workflow.

The current demo has two routes: `/shop` is a CRUD-based product catalog admin surface, and `/showcase` is a database comparison view for storage shape, schema evolution, update behavior, and aggregation.

## What This Demo Shows

- Same domain, same endpoints, two persistence models.
- Full product CRUD from the frontend through a form-based shop detail dialog.
- MongoDB as embedded product documents with local product context.
- PostgreSQL as normalized relational tables with explicit structure.
- Schema evolution through older products without `regionalTaxCode` and newer products with it.
- Update contrast through a category rename scenario.
- Analytics contrast through average price and average rating aggregations.
- MongoDB replica-set failover with visible primary metadata.
- A deliberate CAP/consistency showcase path using weak `w=1` writes.

The CAP scenario is a controlled demonstration of configuration trade-offs, not a claim that MongoDB is generally inconsistent. With stronger write concern such as `majority`, the durability behavior changes and availability under failure becomes more constrained.

## Run With Docker

```powershell
docker compose up --build
```

The default stack now starts three API backends: local MongoDB replica set, MongoDB Atlas, and PostgreSQL. The Atlas backend expects the `MONGO_ATLAS_*` variables in `.env` to be set.

Open the frontend at:

```text
http://localhost:3000/shop
```

The database showcase is available at:

```text
http://localhost:3000/showcase
```

Backend endpoints:

```text
MongoDB API:      http://localhost:5000/api
MongoDB Atlas API:http://localhost:5002/api
PostgreSQL API:  http://localhost:5001/api
MongoDB members: localhost:27117, localhost:27118, localhost:27119
```

The Docker stack starts MongoDB as a replica set named `rs0` with `mongo1`, `mongo2`, and an arbiter. The Mongo backend uses `MONGO_WRITE_CONCERN=1` by default so the failover and rollback showcase remains demonstrable.

## Atlas Seed And Collection Creation

The Atlas collection does not need to be created manually. The seed script creates the target collection automatically on first write and replaces its contents with the demo dataset.

Seed Atlas once explicitly with:

```powershell
docker compose --profile atlas-seed run --rm seed-mongo-atlas
```

This command writes the demo products into `MONGO_ATLAS_DB`.`MONGO_ATLAS_COLLECTION`, creates the collection if it does not exist yet, and recreates the demo indexes.

## CAP Showcase Commands

Start the stack and open `/shop`. The health pills show the current MongoDB primary and write concern.

For the automated rollback/loss lab, run:

```powershell
npm run demo:cap:mongo
```

The script pauses the secondary, performs one weak `w=1` write, stops the current primary, resumes the secondary, waits for election, and verifies whether the acknowledged write survived.

To stop the current primary, first check the primary in the UI or through health:

```powershell
curl http://localhost:5000/api/health
```

Then stop the corresponding container, for example:

```powershell
docker stop mongodb-demo-mongo1
```

After election, continue creating or editing a product in `/shop` or use the consistency lab in `/showcase`. For the destructive rollback/loss demonstration, the seminar flow is the same sequence the CLI automates: pause the secondary before a `w=1` write, stop the primary, resume the secondary, and verify that the acknowledged write can disappear. Reset with:

```powershell
docker compose down -v
docker compose up --build
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

Open `http://localhost:3000/shop` or `http://localhost:3000/showcase`.

Run a backend manually against a local MongoDB instance, for example:

```powershell
set DB_ENGINE=mongo&& set PORT=5000&& set MONGO_URI=mongodb://localhost:27117/?directConnection=true&& python -m backend.app
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

The rename, migration, and CRUD commands are state-changing. Use the seed scripts or restart the Docker stack when you want to return to the original data state.

## Tests

```powershell
python -m pytest
npm --prefix frontend run build
```

## Data Model

MongoDB stores one product as one aggregate document with embedded categories, attributes, variants, highlights, and latest reviews.

PostgreSQL stores the same product through normalized tables: `products`, `manufacturers`, `categories`, `product_categories`, `product_attributes`, `product_variants`, `product_highlights`, and `product_reviews`.

Both backends expose the same high-level product JSON to the frontend so the comparison remains about data-model trade-offs, not about different application features.
# Demo Flow

## Standard Presentation Path

Start the containerized demo first:

```powershell
cd mongodb_demo
docker compose up --build
```

1. Start at `http://localhost:3000` and point out the mixed product list.
2. Select a laptop and show the full document with shared fields and `attributes`.
3. Switch to the Query tab and show the `find` call for the selected document.
4. Switch to the PyMongo tab and show the matching `find_one` call.
5. Reset selection by changing filters: product type `laptop`, RAM from `32 GB`, schema `with regionalTaxCode`.
6. Show that the list, query text, and code text changed together.
7. Select a document without `regionalTaxCode`, then one with `regionalTaxCode`, and use the schema hint above the document.
8. Open the aggregation panel and switch between average price by product type and count by category.
9. Insert a sample product and show that the product count and detail panel update from real MongoDB data.

## Quick Smoke Test

1. `GET /api/health` returns `ok: true`.
2. Product list loads with at least five product types.
3. Selecting a product loads the detail JSON.
4. Aggregation table contains rows.
5. Insert Sample creates and selects a new product.

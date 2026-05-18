# Demo Flow

## 15-Minute Structure

1. Motivation, 1 minute
   Explain that both systems model the same product catalog, but optimize for different kinds of change.

2. Catalog, 2 minutes
   Open the frontend and switch between MongoDB and PostgreSQL. Show that the API and visible product data stay the same.

3. Storage Shape, 3 minutes
   Select a product and compare the document view with the relational shape. Emphasize aggregate locality for MongoDB and explicit table structure for PostgreSQL.

4. Schema Evolution, 3 minutes
   Use the schema filter or the lazy migration scenario. Show older products without `regionalTaxCode` and newer products with it.

5. Update Scenario, 3 minutes
   Run the category rename scenario for both backends. Contrast embedded category copies in MongoDB with one central category row in PostgreSQL.

6. Analytics, 2 minutes
   Run average price by type or average rating by manufacturer. Show that both can answer the question, but the query shape differs.

7. Closing, 1 minute
   State the takeaway: MongoDB and PostgreSQL are both viable here; the right choice depends on workload shape, update patterns, schema volatility, and consistency needs.

## Recommended Live Path

Start the stack:

```powershell
docker compose up --build
```

Open:

```text
http://localhost:5173
```

Then follow this sequence:

1. Keep MongoDB selected and click through the story steps from top to bottom.
2. Select a laptop with schema version 1, then run lazy migration.
3. Switch to PostgreSQL and repeat the same scenario.
4. Run category rename on MongoDB and PostgreSQL.
5. Show analytics once on both backends.

## CLI Backup Path

If the frontend is unavailable, use these commands after starting Docker:

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

The CLI prints the scenario result and the query text, so it can be used as a compact fallback for the live talk.

## Speaker Notes

- Say "this demonstrates a modeling consequence", not "this proves database X is faster".
- Mention that replication, sharding, and failure behavior are deliberately excluded from the live demo.
- Keep the comparison symmetric: first show same visible behavior, then explain the internal difference.
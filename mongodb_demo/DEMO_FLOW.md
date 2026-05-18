# Demo Flow

## 15-Minute Structure

1. Motivation, 1 minute
   Explain that both systems model the same product catalog behind the same JSON contract.

2. CRUD shop, 4 minutes
   Open `/shop`, switch between MongoDB and PostgreSQL, and create, inspect, edit, and delete one product through the JSON dialog.

3. Database showcase, 4 minutes
   Open `/showcase`, select one product, and compare document view, storage shape, schema evolution, query, and code.

4. Update and analytics, 3 minutes
   Run lazy migration or category rename, then show one aggregation on both backends.

5. CAP/failover showcase, 2 minutes
   Stay on MongoDB, stop the current primary container, wait for election, and continue a write in `/shop`.

6. Consistency caveat, 1 minute
   Explain that the destructive rollback/loss path requires weak `w=1` writes and a controlled failover sequence. Majority write concern changes the outcome.

7. Closing, 1 minute
   State the takeaway: MongoDB and PostgreSQL are both viable here; the right choice depends on workload shape, update patterns, schema volatility, and consistency needs.

## Recommended Live Path

Start the stack:

```powershell
docker compose up --build
```

Open:

```text
http://localhost:3000/shop
```

Then follow this sequence:

1. In `/shop`, create a manual product on MongoDB, edit one JSON field, and delete it.
2. Switch to PostgreSQL and repeat the same CRUD flow.
3. Open `/showcase` and compare one laptop on MongoDB and PostgreSQL.
4. Run lazy migration or category rename on both backends.
5. Show analytics once on both backends.
6. Switch back to MongoDB, note the displayed primary, stop that container, wait for election, and perform another shop write.

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

The CLI prints the scenario result and the query text, so it can be used as a compact fallback for the modeling part of the live talk.

## Speaker Notes

- Say "this demonstrates a modeling consequence", not "this proves database X is faster".
- For CAP, name the exact MongoDB configuration: replica set, `w=1` for the weak-write path, or `majority` for the stronger consistency path.
- Say "this shows a configured consistency/availability trade-off", not "MongoDB is inconsistent".
- Keep the comparison symmetric: first show same visible behavior, then explain the internal difference.
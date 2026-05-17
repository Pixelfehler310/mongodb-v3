# Demo Project Requirements

## Purpose

This document defines the target requirements for the new demo project used in a seminar paper presentation for the NoSQL Databases module.

The project is intentionally small, visual, and easy to explain. It is not the scientific benchmark core of the work. Its purpose is to make MongoDB concepts visible and understandable in a short live presentation.

## Relationship to the Scientific Repo

This repository is the demo companion to `mongodb-v2`.

The scientific comparison, hypotheses, and benchmark evidence belong in the other repo. This repo exists to explain MongoDB clearly through a product-catalog example.

## Core Goal

The demo shall allow a presenter to show:

1. real MongoDB product documents,
2. polymorphic product types in one collection,
3. filters over simple, nested, and array fields,
4. the corresponding MongoDB query,
5. the corresponding PyMongo code,
6. at least one simple aggregation,
7. a small schema-evolution story.

## Domain

The recommended demo domain is a product catalog.

The catalog should include multiple product families with shared base fields and product-specific attributes.

Recommended product families:

- laptops
- t-shirts
- books
- smartphones
- desks

This domain is preferred because it demonstrates:

- nested documents,
- arrays,
- optional and polymorphic fields,
- schema flexibility,
- easy-to-explain filters,
- simple aggregations.

## Example Document Shape

```json
{
  "_id": "prod_1001",
  "productId": "prod_1001",
  "sku": "LAP-1001",
  "productType": "laptop",
  "name": "Aster Pro 14",
  "basePrice": 1499.0,
  "currency": "EUR",
  "manufacturer": {
    "id": "man_010",
    "name": "Northstar Computing"
  },
  "categories": [
    { "id": "cat_001", "name": "Laptops", "slug": "laptops" }
  ],
  "attributes": {
    "cpuModel": "Ryzen 7 8840U",
    "ramGb": 32,
    "storageGb": 1000,
    "screenSizeInches": 14
  },
  "variants": [
    { "variantId": "var_1", "label": "32 GB / 1 TB", "inventoryCount": 18 }
  ],
  "latestReviews": [
    { "reviewId": "rev_01", "rating": 5, "title": "Fast and quiet" }
  ],
  "regionalTaxCode": "DE-STD",
  "updatedAt": "2026-05-17T10:15:00Z"
}
```

## Scope

The project shall be a small web application connected to MongoDB.

It should provide:

- a simple product list,
- a compact filter area,
- a detail panel for the selected document,
- visible query text,
- visible PyMongo code,
- at least one aggregation view.

The project shall not try to cover:

- SQL comparison,
- benchmarking,
- authentication,
- multi-user workflows,
- production-hardening,
- generic admin tooling.

## Main Presentation Scenario

A presenter opens the application and shows this flow:

1. browse products,
2. switch between different product types,
3. open one product and inspect the full document,
4. explain the current MongoDB query,
5. show the matching PyMongo code,
6. run a small aggregation,
7. optionally show a document with a newer schema field.

## Functional Requirements

### FR1. Product List

The system shall display a list of products from MongoDB.

The list shall:

1. show a limited initial result set,
2. support selecting one item,
3. show the product type,
4. show the name, price, manufacturer, and at least one category.

### FR2. Detail View

The system shall display the full selected product document.

The detail view shall:

1. stay close to stored JSON,
2. make nested objects visible,
3. make arrays visible,
4. clearly expose product-specific attributes.

### FR3. Filtering

The system shall support a small set of explainable filters.

Mandatory filters:

1. `productType`
2. manufacturer
3. category
4. price range
5. one nested field

Optional filters:

1. search over product name
2. tag-like array filter
3. schema-version or evolution marker

### FR4. Combined Filters

Multiple filters shall be combinable.

Results and query display shall update together.

### FR5. Query Display

The system shall display the MongoDB query matching the current UI state.

It shall:

1. update automatically,
2. remain readable,
3. match the visible result set,
4. use realistic MongoDB syntax.

### FR6. Code Display

The system shall display a short PyMongo code example for the current action.

It shall:

1. be short,
2. be didactic,
3. stay consistent in Python style,
4. avoid unnecessary production complexity.

### FR7. Aggregation Demo

The system shall include at least two simple aggregations.

Suitable examples:

1. average price by product type,
2. product count by manufacturer,
3. product count by category,
4. average rating by product type.

### FR8. Schema Evolution Visibility

The demo shall make at least one schema evolution aspect visible.

Recommended example:

- some products contain `regionalTaxCode` while older ones do not.

### FR9. Stable Local Setup

The project shall support a short local startup flow:

1. start MongoDB,
2. seed demo data,
3. start the Flask app,
4. open the UI,
5. begin the presentation.

## Non-Functional Requirements

### NFR1. Simplicity

Simplicity is the highest priority.

### NFR2. Presentability

The demo shall be reliable enough for a short seminar presentation.

### NFR3. Understandability

The demo shall be understandable for an audience that does not know the codebase.

### NFR4. Small Architecture

The data flow should remain easy to explain:

`Browser UI -> Flask API -> PyMongo repository -> MongoDB`

## Implementation Direction

The preferred implementation style remains close to the current repository setup:

- Flask backend,
- PyMongo repository layer,
- deterministic Python seeding,
- simple HTML/CSS/JavaScript frontend.

The detailed implementation target is defined in:

- `SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md`
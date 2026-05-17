# Demo Project Specification Snapshot

The full source specification is stored in the workspace root as `SEMINARARBEIT_DEMOPROJEKT_SPEZIFIKATION.md`.

This project implements the requested target shape:

- Flask backend
- PyMongo repository layer
- deterministic Python seeding
- vanilla HTML/CSS/JavaScript frontend
- local MongoDB through Docker Compose
- product catalog domain with five polymorphic product families
- query and code display for list and detail actions
- aggregation panel with multiple aggregation kinds
- schema-evolution visibility through `regionalTaxCode`
- live sample insert through `POST /api/products/sample`

The demo intentionally does not include benchmark logic or SQL comparison code.

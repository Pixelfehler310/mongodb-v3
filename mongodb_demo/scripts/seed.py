from __future__ import annotations

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from mongodb_demo.backend.database import MongoDatabase
from mongodb_demo.backend.sample_data import generate_products
from mongodb_demo.backend.settings import Settings


def create_indexes(collection) -> None:
    collection.create_index("productType")
    collection.create_index("manufacturer.name")
    collection.create_index("categories.slug")
    collection.create_index("updatedAt")
    collection.create_index("attributes.ramGb")
    collection.create_index("shipping.availableRegions")


def main() -> None:
    settings = Settings.from_env()
    database = MongoDatabase(settings)
    products = generate_products(count=300)
    database.collection.drop()
    database.collection.insert_many(products)
    create_indexes(database.collection)
    print(f"Seeded {len(products)} products into {settings.mongo_db}.{settings.mongo_collection}")
    database.close()


if __name__ == "__main__":
    main()
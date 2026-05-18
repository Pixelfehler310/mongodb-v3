from __future__ import annotations

from typing import Any

from .mongo_repository import MongoProductRepository
from .postgres_repository import PostgresProductRepository


def create_repository(database: Any, engine: str) -> MongoProductRepository | PostgresProductRepository:
    if engine == "postgres":
        return PostgresProductRepository(database)
    return MongoProductRepository(database)
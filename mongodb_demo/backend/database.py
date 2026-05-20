from __future__ import annotations

from .mongo_database import MongoDatabase
from .postgres_database import PostgresDatabase
from .settings import Settings


def create_database(settings: Settings) -> MongoDatabase | PostgresDatabase:
    if settings.db_engine == "postgres":
        return PostgresDatabase(settings)
    if settings.db_engine == "mongo":
        return MongoDatabase(settings)
    raise ValueError(f"Unsupported DB_ENGINE: {settings.db_engine}")

from __future__ import annotations

import importlib
from typing import Any

from pymongo import MongoClient

from .settings import Settings


psycopg: Any = importlib.import_module("psycopg")
dict_row: Any = importlib.import_module("psycopg.rows").dict_row


class MongoDatabase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
        self.database = self.client[settings.mongo_db]
        self.collection = self.database[settings.mongo_collection]

    def ping(self) -> bool:
        self.client.admin.command("ping")
        return True

    def close(self) -> None:
        self.client.close()


class PostgresDatabase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection: Any = psycopg.connect(settings.postgres_dsn, row_factory=dict_row)
        self.connection.autocommit = True

    def ping(self) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True

    def close(self) -> None:
        self.connection.close()


def create_database(settings: Settings) -> MongoDatabase | PostgresDatabase:
    if settings.db_engine == "postgres":
        return PostgresDatabase(settings)
    if settings.db_engine == "mongo":
        return MongoDatabase(settings)
    raise ValueError(f"Unsupported DB_ENGINE: {settings.db_engine}")
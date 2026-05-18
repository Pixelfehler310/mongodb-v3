from __future__ import annotations

import importlib
from typing import Any

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

from .settings import Settings


psycopg: Any = importlib.import_module("psycopg")
dict_row: Any = importlib.import_module("psycopg.rows").dict_row


class MongoDatabase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
        self.database = self.client[settings.mongo_db]
        self.collection = self.database.get_collection(
            settings.mongo_collection,
            write_concern=WriteConcern(w=_write_concern_value(settings.mongo_write_concern)),
            read_concern=ReadConcern(settings.mongo_read_concern),
            read_preference=_read_preference_value(settings.mongo_read_preference),
        )

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


def _write_concern_value(value: str) -> int | str:
    cleaned_value = value.strip()
    if cleaned_value.isdigit():
        return int(cleaned_value)
    return cleaned_value


def _read_preference_value(value: str) -> Any:
    preferences = {
        "primary": ReadPreference.PRIMARY,
        "primarypreferred": ReadPreference.PRIMARY_PREFERRED,
        "secondary": ReadPreference.SECONDARY,
        "secondarypreferred": ReadPreference.SECONDARY_PREFERRED,
        "nearest": ReadPreference.NEAREST,
    }
    return preferences.get(value.replace("_", "").replace("-", "").lower(), ReadPreference.PRIMARY)
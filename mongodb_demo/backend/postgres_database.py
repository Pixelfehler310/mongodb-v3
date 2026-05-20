from __future__ import annotations

import importlib
from typing import Any

from .settings import Settings


psycopg: Any = importlib.import_module("psycopg")
dict_row: Any = importlib.import_module("psycopg.rows").dict_row


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
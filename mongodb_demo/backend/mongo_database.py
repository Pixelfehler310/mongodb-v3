from __future__ import annotations

from typing import Any

from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

from .settings import Settings


class MongoDatabase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
        self.database = self.client[settings.mongo_db]
        # These options make the demo's consistency behavior explicit and configurable via env vars.
        self.collection = self.database.get_collection(
            settings.mongo_collection,
            write_concern=WriteConcern(
                w=_write_concern_value(settings.mongo_write_concern)
            ),
            read_concern=ReadConcern(settings.mongo_read_concern),
            read_preference=_read_preference_value(settings.mongo_read_preference),
        )

    def ping(self) -> bool:
        self.client.admin.command("ping")
        return True

    def close(self) -> None:
        self.client.close()


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
    return preferences.get(
        value.replace("_", "").replace("-", "").lower(), ReadPreference.PRIMARY
    )

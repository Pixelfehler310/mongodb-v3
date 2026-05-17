from __future__ import annotations

from pymongo import MongoClient

from .settings import Settings


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
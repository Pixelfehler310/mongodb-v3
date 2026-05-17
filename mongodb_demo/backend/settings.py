from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    port: int
    mongo_uri: str
    mongo_db: str
    mongo_collection: str
    default_limit: int
    seed_profile: str
    enable_evolution_view: bool

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            port=int(os.getenv("PORT", "3000")),
            mongo_uri=os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
            mongo_db=os.getenv("MONGO_DB", "product_demo"),
            mongo_collection=os.getenv("MONGO_COLLECTION", "products"),
            default_limit=int(os.getenv("DEFAULT_LIMIT", "25")),
            seed_profile=os.getenv("DEMO_SEED_PROFILE", "standard"),
            enable_evolution_view=os.getenv("ENABLE_EVOLUTION_VIEW", "true").lower()
            in {"1", "true", "yes", "on"},
        )
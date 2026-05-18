from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    port: int
    db_engine: str
    mongo_uri: str
    mongo_db: str
    mongo_collection: str
    mongo_write_concern: str
    mongo_read_concern: str
    mongo_read_preference: str
    postgres_dsn: str
    default_limit: int

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            port=int(os.getenv("PORT", "3000")),
            db_engine=os.getenv("DB_ENGINE", "mongo").strip().lower(),
            mongo_uri=os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
            mongo_db=os.getenv("MONGO_DB", "product_demo"),
            mongo_collection=os.getenv("MONGO_COLLECTION", "products"),
            mongo_write_concern=os.getenv("MONGO_WRITE_CONCERN", "1"),
            mongo_read_concern=os.getenv("MONGO_READ_CONCERN", "local"),
            mongo_read_preference=os.getenv("MONGO_READ_PREFERENCE", "primary"),
            postgres_dsn=os.getenv("POSTGRES_DSN", "postgresql://benchmark:benchmark@localhost:5433/product_demo"),
            default_limit=int(os.getenv("DEFAULT_LIMIT", "12")),
        )
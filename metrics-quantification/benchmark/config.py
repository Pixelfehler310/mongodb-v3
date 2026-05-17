from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_pool_min: int
    postgres_pool_max: int
    mongo_uri: str
    mongo_db: str
    mongo_max_pool_size: int
    export_dir: Path
    log_level: str
    default_dataset: str

    @property
    def postgres_dsn(self) -> str:
        return (
            f"host={self.postgres_host} port={self.postgres_port} dbname={self.postgres_db} "
            f"user={self.postgres_user} password={self.postgres_password}"
        )


def load_settings(env_file: str | None = None) -> Settings:
    load_dotenv(env_file)
    return Settings(
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        postgres_db=os.getenv("POSTGRES_DB", "product_benchmark"),
        postgres_user=os.getenv("POSTGRES_USER", "benchmark"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "benchmark"),
        postgres_pool_min=int(os.getenv("POSTGRES_POOL_MIN", "1")),
        postgres_pool_max=int(os.getenv("POSTGRES_POOL_MAX", "20")),
        mongo_uri=os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
        mongo_db=os.getenv("MONGO_DB", "product_benchmark"),
        mongo_max_pool_size=int(os.getenv("MONGO_MAX_POOL_SIZE", "50")),
        export_dir=Path(os.getenv("EXPORT_DIR", "./exports/raw")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        default_dataset=os.getenv("BENCHMARK_DEFAULT_DATASET", "small"),
    )

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from benchmark.seed.generator import Catalog


class BenchmarkAdapter(ABC):
    database_type: str

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def seed(self, catalog: Catalog) -> None:
        raise NotImplementedError

    @abstractmethod
    def validate(self, expected_counts: dict[str, int]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def sample_product_ids(self, limit: int) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def sample_category_ids(self, limit: int) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def read_product_aggregate(self, product_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def rename_category(self, category_id: str, new_name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def analytical_query(self, limit: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    def explain_summary(self, scenario_id: str) -> dict[str, Any]:
        return {"scenario_id": scenario_id, "available": False}

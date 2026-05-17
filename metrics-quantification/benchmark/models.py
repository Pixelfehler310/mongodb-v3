from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class DatasetProfile:
    name: str
    products: int
    variants: int
    reviews: int
    categories: int
    manufacturers: int

    def as_counts(self) -> dict[str, int]:
        return {
            "products": self.products,
            "variants": self.variants,
            "reviews": self.reviews,
            "categories": self.categories,
            "manufacturers": self.manufacturers,
        }


@dataclass(frozen=True)
class WorkloadDefinition:
    scenario_id: str
    display_name: str
    query_family: str
    dataset_profile: str
    default_repetitions: int
    default_operations: int
    supports_explain: bool


@dataclass
class OperationResult:
    operation: str
    success: bool
    latency_ms: float
    error_class: str | None = None
    error_message: str | None = None


@dataclass
class WorkloadRun:
    run_id: str
    timestamp_utc: str
    scenario_id: str
    scenario_name: str
    database_type: str
    dataset_profile: str
    repetition_index: int
    seed: int
    warmup_used: bool
    total_operations: int
    operation_results: list[OperationResult] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        run_id: str,
        scenario: WorkloadDefinition,
        database_type: str,
        dataset_profile: str,
        repetition_index: int,
        seed: int,
        warmup_used: bool,
        total_operations: int,
    ) -> "WorkloadRun":
        return cls(
            run_id=run_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            scenario_id=scenario.scenario_id,
            scenario_name=scenario.display_name,
            database_type=database_type,
            dataset_profile=dataset_profile,
            repetition_index=repetition_index,
            seed=seed,
            warmup_used=warmup_used,
            total_operations=total_operations,
        )

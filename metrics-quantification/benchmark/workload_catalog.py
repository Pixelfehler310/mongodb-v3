from __future__ import annotations

from benchmark.models import WorkloadDefinition


SCENARIOS: dict[str, WorkloadDefinition] = {
    "read-locality": WorkloadDefinition(
        scenario_id="read-locality",
        display_name="Read Locality Advantage",
        query_family="aggregate-read",
        dataset_profile="small",
        default_repetitions=5,
        default_operations=100,
        supports_explain=True,
    ),
    "denormalized-update": WorkloadDefinition(
        scenario_id="denormalized-update",
        display_name="Denormalized Update Cost",
        query_family="category-rename",
        dataset_profile="small",
        default_repetitions=5,
        default_operations=10,
        supports_explain=False,
    ),
    "join-lookup": WorkloadDefinition(
        scenario_id="join-lookup",
        display_name="Join versus Lookup Pressure",
        query_family="analytical-join-lookup",
        dataset_profile="small",
        default_repetitions=5,
        default_operations=25,
        supports_explain=True,
    ),
}


def scenario_list(selection: str) -> list[WorkloadDefinition]:
    if selection == "all":
        return list(SCENARIOS.values())
    return [SCENARIOS[selection]]

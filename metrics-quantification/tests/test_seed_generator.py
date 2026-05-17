from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.seed.generator import DATASET_PROFILES, generate_catalog


def test_generate_catalog_is_deterministic_for_same_seed():
    profile = DATASET_PROFILES["tiny"]
    first = generate_catalog(profile, seed=123)
    second = generate_catalog(profile, seed=123)

    assert first.products == second.products
    assert first.variants == second.variants
    assert first.reviews == second.reviews


def test_generate_catalog_matches_profile_counts():
    profile = DATASET_PROFILES["tiny"]
    catalog = generate_catalog(profile, seed=42)

    assert len(catalog.products) == profile.products
    assert len(catalog.variants) == profile.variants
    assert len(catalog.reviews) == profile.reviews
    assert len(catalog.categories) == profile.categories
    assert len(catalog.manufacturers) == profile.manufacturers

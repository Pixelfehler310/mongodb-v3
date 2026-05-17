from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from faker import Faker

from benchmark.models import DatasetProfile


DATASET_PROFILES: dict[str, DatasetProfile] = {
    "tiny": DatasetProfile("tiny", products=20, variants=60, reviews=100, categories=8, manufacturers=6),
    "small": DatasetProfile("small", products=5_000, variants=20_000, reviews=50_000, categories=200, manufacturers=500),
    "large": DatasetProfile("large", products=100_000, variants=400_000, reviews=1_000_000, categories=1_000, manufacturers=5_000),
}

PRODUCT_TYPES = ["laptop", "tshirt", "book", "smartphone", "desk"]


@dataclass(frozen=True)
class Catalog:
    manufacturers: list[dict[str, Any]]
    categories: list[dict[str, Any]]
    products: list[dict[str, Any]]
    variants: list[dict[str, Any]]
    reviews: list[dict[str, Any]]


def generate_catalog(profile: DatasetProfile, seed: int) -> Catalog:
    faker = Faker()
    Faker.seed(seed)
    rng = random.Random(seed)
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    manufacturers = _manufacturers(profile.manufacturers, rng)
    categories = _categories(profile.categories)
    products = [_product(index, manufacturers, categories, faker, rng, base_time) for index in range(profile.products)]
    variant_counts = _weighted_counts(profile.variants, profile.products, hot_every=25, hot_weight=3)
    review_counts = _weighted_counts(profile.reviews, profile.products, hot_every=20, hot_weight=8)
    variants = [variant for product_index, count in enumerate(variant_counts) for variant in _variants(product_index, count, rng)]
    reviews = [review for product_index, count in enumerate(review_counts) for review in _reviews(product_index, count, rng, base_time)]
    return Catalog(manufacturers=manufacturers, categories=categories, products=products, variants=variants, reviews=reviews)


def _manufacturers(count: int, rng: random.Random) -> list[dict[str, str]]:
    countries = ["DE", "US", "CN", "JP", "NL", "FR", "SE"]
    return [
        {"manufacturer_id": f"mfg-{index:05d}", "name": f"Manufacturer {index:05d}", "country": rng.choice(countries)}
        for index in range(count)
    ]


def _categories(count: int) -> list[dict[str, str | None]]:
    categories = []
    for index in range(count):
        parent = None if index < 10 else f"cat-{index % 10:04d}"
        categories.append({"category_id": f"cat-{index:04d}", "name": f"Category {index:04d}", "slug": f"category-{index:04d}", "parent_category_id": parent})
    return categories


def _product(index: int, manufacturers: list[dict[str, Any]], categories: list[dict[str, Any]], faker: Faker, rng: random.Random, base_time: datetime) -> dict[str, Any]:
    product_type = rng.choices(PRODUCT_TYPES, weights=[18, 28, 20, 18, 16], k=1)[0]
    category_count = 1 + (index % 3)
    category_ids = [categories[(index + offset * 7) % len(categories)]["category_id"] for offset in range(category_count)]
    created_at = base_time + timedelta(minutes=index)
    return {
        "product_id": f"prod-{index:07d}",
        "sku": f"SKU-{index:07d}",
        "product_type": product_type,
        "name": f"{product_type.title()} {faker.word().title()} {index:05d}",
        "base_price": round(rng.uniform(9.99, 2499.99), 2),
        "currency": "EUR",
        "manufacturer_id": manufacturers[index % len(manufacturers)]["manufacturer_id"],
        "category_ids": category_ids,
        "status": "active" if index % 17 else "archived",
        "regional_tax_code": "EU-DE-STD" if index % 2 == 0 else "EU-DE-REDUCED",
        "created_at": created_at,
        "updated_at": created_at + timedelta(days=index % 30),
        "type_attributes": _type_attributes(product_type, index, rng),
    }


def _type_attributes(product_type: str, index: int, rng: random.Random) -> dict[str, Any]:
    if product_type == "laptop":
        return {"cpu_model": rng.choice(["Ryzen 7", "Core i7", "M3"]), "ram_gb": rng.choice([16, 32, 64]), "storage_gb": rng.choice([512, 1024, 2048]), "gpu_model": rng.choice(["Integrated", "RTX 4060", "RX 7600M"]), "screen_size_inches": rng.choice([13.3, 14.0, 15.6, 16.0])}
    if product_type == "tshirt":
        return {"size": rng.choice(["S", "M", "L", "XL"]), "material": rng.choice(["cotton", "linen", "polyester"]), "fit": rng.choice(["regular", "slim", "oversized"]), "color": rng.choice(["black", "white", "blue", "green"]), "target_group": rng.choice(["men", "women", "unisex"])}
    if product_type == "book":
        return {"author": f"Author {index % 1000}", "isbn": f"978-3-{index % 10}-{index:07d}-0", "page_count": rng.randint(120, 900), "language": rng.choice(["de", "en", "fr"]), "publisher": f"Publisher {index % 50}"}
    if product_type == "smartphone":
        return {"soc": rng.choice(["A18", "Tensor G5", "Snapdragon 8"]), "display_inches": rng.choice([6.1, 6.4, 6.7]), "battery_mah": rng.choice([4200, 4800, 5200]), "camera_mp": rng.choice([48, 50, 108]), "os_family": rng.choice(["Android", "iOS"])}
    return {"material": rng.choice(["oak", "steel", "bamboo"]), "width_cm": rng.choice([120, 140, 160]), "height_cm": rng.choice([72, 75]), "depth_cm": rng.choice([60, 80]), "max_load_kg": rng.choice([60, 80, 120])}


def _variants(product_index: int, count: int, rng: random.Random) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": f"var-{product_index:07d}-{variant_index:03d}",
            "product_id": f"prod-{product_index:07d}",
            "label": f"Variant {variant_index + 1}",
            "price_delta": round(rng.uniform(-25.0, 250.0), 2),
            "inventory_count": rng.randint(0, 500),
            "variant_attributes": {"color": rng.choice(["black", "white", "blue", "green"]), "size": rng.choice(["S", "M", "L", "XL", "one-size"])},
        }
        for variant_index in range(count)
    ]


def _reviews(product_index: int, count: int, rng: random.Random, base_time: datetime) -> list[dict[str, Any]]:
    return [
        {
            "review_id": f"rev-{product_index:07d}-{review_index:04d}",
            "product_id": f"prod-{product_index:07d}",
            "user_id": f"user-{rng.randint(1, 250_000):07d}",
            "rating": rng.choices([1, 2, 3, 4, 5], weights=[4, 8, 16, 34, 38], k=1)[0],
            "title": "Deterministic review",
            "text": "Generated benchmark review text.",
            "created_at": base_time + timedelta(hours=review_index, minutes=product_index),
            "verified_purchase": review_index % 4 != 0,
        }
        for review_index in range(count)
    ]


def _weighted_counts(total: int, buckets: int, hot_every: int, hot_weight: int) -> list[int]:
    weights = [hot_weight if index % hot_every == 0 else 1 for index in range(buckets)]
    weight_sum = sum(weights)
    counts = [(total * weight) // weight_sum for weight in weights]
    remainder = total - sum(counts)
    for index in range(remainder):
        counts[index % buckets] += 1
    return counts

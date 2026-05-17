from __future__ import annotations

import copy
import random
from datetime import datetime, timedelta, timezone
from typing import Any


PRODUCT_TYPES = ["laptop", "t-shirt", "book", "smartphone", "desk"]

MANUFACTURERS = [
    {"id": "man_001", "name": "Northstar Computing", "types": ["laptop", "smartphone"]},
    {"id": "man_002", "name": "Aster Devices", "types": ["laptop", "smartphone"]},
    {"id": "man_003", "name": "Cobalt Systems", "types": ["laptop"]},
    {"id": "man_004", "name": "Urban Loom", "types": ["t-shirt"]},
    {"id": "man_005", "name": "Green Thread", "types": ["t-shirt"]},
    {"id": "man_006", "name": "Plain Cotton Co", "types": ["t-shirt"]},
    {"id": "man_007", "name": "Blue Harbor Books", "types": ["book"]},
    {"id": "man_008", "name": "Atlas Academic Press", "types": ["book"]},
    {"id": "man_009", "name": "Paper Trail Verlag", "types": ["book"]},
    {"id": "man_010", "name": "Pocket Galaxy", "types": ["smartphone"]},
    {"id": "man_011", "name": "Signal Works", "types": ["smartphone"]},
    {"id": "man_012", "name": "Oak & Steel", "types": ["desk"]},
    {"id": "man_013", "name": "Nordic Office", "types": ["desk"]},
    {"id": "man_014", "name": "FlexFrame", "types": ["desk"]},
    {"id": "man_015", "name": "Juniper Goods", "types": PRODUCT_TYPES},
    {"id": "man_016", "name": "Metro Supply", "types": PRODUCT_TYPES},
    {"id": "man_017", "name": "Rhein Retail", "types": PRODUCT_TYPES},
    {"id": "man_018", "name": "Kite Commerce", "types": PRODUCT_TYPES},
    {"id": "man_019", "name": "Polar Line", "types": PRODUCT_TYPES},
    {"id": "man_020", "name": "Mosaic Market", "types": PRODUCT_TYPES},
]

CATEGORIES = {
    "laptop": [{"id": "cat_001", "name": "Laptops", "slug": "laptops"}],
    "t-shirt": [{"id": "cat_002", "name": "T-Shirts", "slug": "t-shirts"}],
    "book": [{"id": "cat_003", "name": "Books", "slug": "books"}],
    "smartphone": [{"id": "cat_004", "name": "Smartphones", "slug": "smartphones"}],
    "desk": [{"id": "cat_005", "name": "Desks", "slug": "desks"}],
}

SECONDARY_CATEGORIES = [
    {"id": "cat_010", "name": "Home Office", "slug": "home-office"},
    {"id": "cat_011", "name": "Student Picks", "slug": "student-picks"},
    {"id": "cat_012", "name": "New Arrivals", "slug": "new-arrivals"},
    {"id": "cat_013", "name": "Sustainable", "slug": "sustainable"},
    {"id": "cat_014", "name": "Premium", "slug": "premium"},
    {"id": "cat_015", "name": "Travel Friendly", "slug": "travel-friendly"},
]

TYPE_CONFIG = {
    "laptop": {"prefix": "LAP", "base": (799, 2499), "names": ["Aster Pro", "Northbook", "Cobalt Air", "Juniper Work"]},
    "t-shirt": {"prefix": "TSH", "base": (18, 79), "names": ["Everyday Tee", "Harbor Shirt", "Loom Classic", "Metro Crew"]},
    "book": {"prefix": "BOK", "base": (12, 89), "names": ["Data Patterns", "Quiet Systems", "Readable Code", "NoSQL Notes"]},
    "smartphone": {"prefix": "PHN", "base": (299, 1399), "names": ["Pocket One", "Signal X", "Galaxy Lite", "Aster Phone"]},
    "desk": {"prefix": "DSK", "base": (149, 1199), "names": ["Oak Standing Desk", "Nordic Frame", "FlexFrame Pro", "Studio Desk"]},
}

STATUSES = ["available", "limited", "out_of_stock"]
REGIONS = ["DE", "AT", "CH", "NL", "FR"]
TAGS = ["new", "eco", "student", "premium", "compact", "work", "gift", "sale"]


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _manufacturer(product_type: str, rng: random.Random) -> dict[str, str]:
    choices = [item for item in MANUFACTURERS if product_type in item["types"]]
    selected = rng.choice(choices)
    return {"id": selected["id"], "name": selected["name"]}


def _categories(product_type: str, rng: random.Random) -> list[dict[str, str]]:
    categories = copy.deepcopy(CATEGORIES[product_type])
    if rng.random() < 0.65:
        categories.append(copy.deepcopy(rng.choice(SECONDARY_CATEGORIES)))
    if rng.random() < 0.2:
        extra = copy.deepcopy(rng.choice(SECONDARY_CATEGORIES))
        if extra["slug"] not in {category["slug"] for category in categories}:
            categories.append(extra)
    return categories


def _attributes(product_type: str, rng: random.Random, index: int) -> dict[str, Any]:
    if product_type == "laptop":
        return {
            "cpuModel": rng.choice(["Ryzen 7 8840U", "Intel Core Ultra 7", "Apple M3", "Ryzen 5 8640U"]),
            "ramGb": rng.choice([8, 16, 16, 32, 32, 64]),
            "storageGb": rng.choice([256, 512, 1000, 2000]),
            "screenSizeInches": rng.choice([13.3, 14, 15.6, 16]),
            "hasTouchscreen": rng.random() < 0.35,
            "operatingSystem": rng.choice(["Windows 11", "Ubuntu", "macOS"]),
        }
    if product_type == "t-shirt":
        return {
            "size": rng.choice(["XS", "S", "M", "L", "XL"]),
            "material": rng.choice(["organic cotton", "cotton", "linen blend", "recycled polyester"]),
            "color": rng.choice(["black", "white", "forest", "navy", "clay"]),
            "fit": rng.choice(["regular", "slim", "relaxed"]),
            "organicCotton": rng.random() < 0.45,
        }
    if product_type == "book":
        return {
            "author": rng.choice(["Mira Klein", "Jonas Weber", "Lea Hartmann", "Noah Fischer"]),
            "isbn": f"978-3-{index:04d}-{rng.randint(1000, 9999)}",
            "pageCount": rng.choice([184, 236, 312, 428, 520]),
            "language": rng.choice(["de", "en"]),
            "format": rng.choice(["paperback", "hardcover", "ebook"]),
        }
    if product_type == "smartphone":
        return {
            "os": rng.choice(["Android", "iOS"]),
            "storageGb": rng.choice([64, 128, 256, 512, 1000]),
            "cameraMegapixels": rng.choice([12, 24, 48, 64, 108]),
            "screenSizeInches": rng.choice([5.9, 6.1, 6.4, 6.7]),
            "dualSim": rng.random() < 0.55,
        }
    return {
        "widthCm": rng.choice([100, 120, 140, 160, 180]),
        "depthCm": rng.choice([60, 70, 80]),
        "heightAdjustable": rng.random() < 0.5,
        "material": rng.choice(["oak", "bamboo", "steel", "walnut veneer"]),
        "maxLoadKg": rng.choice([60, 80, 100, 120]),
    }


def _variants(product_type: str, rng: random.Random) -> list[dict[str, Any]]:
    count = rng.randint(2, 5) if product_type in {"t-shirt", "smartphone", "laptop"} else rng.randint(1, 3)
    variants = []
    for variant_index in range(1, count + 1):
        variants.append(
            {
                "variantId": f"var_{variant_index}",
                "label": _variant_label(product_type, rng),
                "inventoryCount": rng.randint(0, 90),
            }
        )
    return variants


def _variant_label(product_type: str, rng: random.Random) -> str:
    if product_type == "laptop":
        return rng.choice(["16 GB / 512 GB", "32 GB / 1 TB", "64 GB / 2 TB"])
    if product_type == "t-shirt":
        return rng.choice(["Black / M", "White / L", "Forest / XL", "Navy / S"])
    if product_type == "book":
        return rng.choice(["Paperback", "Hardcover", "Ebook"])
    if product_type == "smartphone":
        return rng.choice(["128 GB", "256 GB", "512 GB", "1 TB"])
    return rng.choice(["120 x 70 cm", "140 x 80 cm", "160 x 80 cm"])


def _reviews(product_id: str, rng: random.Random) -> list[dict[str, Any]]:
    reviews = []
    for index in range(rng.randint(0, 5)):
        reviews.append(
            {
                "reviewId": f"rev_{product_id}_{index + 1}",
                "rating": rng.choice([3, 4, 4, 5, 5]),
                "title": rng.choice(["Fast delivery", "Good value", "Solid choice", "Would buy again", "Nice finish"]),
            }
        )
    return reviews


def _shipping(product_type: str, rng: random.Random) -> dict[str, Any]:
    weight_ranges = {
        "laptop": (1.1, 2.4),
        "t-shirt": (0.15, 0.45),
        "book": (0.25, 1.2),
        "smartphone": (0.18, 0.35),
        "desk": (18.0, 42.0),
    }
    low, high = weight_ranges[product_type]
    return {
        "weightKg": round(rng.uniform(low, high), 2),
        "availableRegions": sorted(rng.sample(REGIONS, rng.randint(2, len(REGIONS)))),
        "leadTimeDays": rng.choice([1, 2, 3, 5, 7, 10]),
        "fragile": product_type in {"laptop", "smartphone", "desk"} and rng.random() < 0.45,
    }


def _price(product_type: str, rng: random.Random) -> float:
    low, high = TYPE_CONFIG[product_type]["base"]
    return round(rng.uniform(low, high), 2)


def _name(product_type: str, rng: random.Random, index: int) -> str:
    base = rng.choice(TYPE_CONFIG[product_type]["names"])
    suffix = rng.choice(["14", "Plus", "Studio", "Core", "Edition", "Lite"])
    return f"{base} {suffix} {index % 11 + 1}"


def build_product(index: int, rng: random.Random) -> dict[str, Any]:
    product_type = PRODUCT_TYPES[index % len(PRODUCT_TYPES)]
    product_id = f"prod_{1000 + index}"
    updated_at = datetime(2026, 5, 17, 10, 0, tzinfo=timezone.utc) - timedelta(hours=index * 3)
    created_at = updated_at - timedelta(days=rng.randint(12, 260))
    config = TYPE_CONFIG[product_type]
    document: dict[str, Any] = {
        "_id": product_id,
        "productId": product_id,
        "sku": f"{config['prefix']}-{1000 + index}",
        "productType": product_type,
        "name": _name(product_type, rng, index),
        "basePrice": _price(product_type, rng),
        "currency": "EUR",
        "manufacturer": _manufacturer(product_type, rng),
        "categories": _categories(product_type, rng),
        "attributes": _attributes(product_type, rng, index),
        "variants": _variants(product_type, rng),
        "highlights": rng.sample(
            ["portable", "durable", "quiet", "modular", "comfortable", "energy efficient", "compact"],
            3,
        ),
        "latestReviews": _reviews(product_id, rng),
        "shipping": _shipping(product_type, rng),
        "tags": sorted(rng.sample(TAGS, rng.randint(2, 4))),
        "status": rng.choices(STATUSES, weights=[0.72, 0.18, 0.10], k=1)[0],
        "schemaVersion": 2 if index % 3 != 0 else 1,
        "createdAt": _iso(created_at),
        "updatedAt": _iso(updated_at),
    }
    if document["schemaVersion"] == 2:
        document["regionalTaxCode"] = rng.choice(["DE-STD", "DE-REDUCED", "EU-DIGITAL"])
        if rng.random() < 0.45:
            document["compliance"] = {"ceMarked": True, "warrantyMonths": rng.choice([12, 24, 36])}
    return document


def generate_products(count: int = 300, seed: int = 42) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    return [build_product(index, rng) for index in range(1, count + 1)]


def build_live_sample(product_type: str = "laptop", sequence: int = 1) -> dict[str, Any]:
    if product_type not in PRODUCT_TYPES:
        product_type = "laptop"
    rng = random.Random(9000 + sequence + PRODUCT_TYPES.index(product_type))
    seed_index = 8000 + (sequence * len(PRODUCT_TYPES)) + PRODUCT_TYPES.index(product_type)
    document = build_product(seed_index, rng)
    product_id = f"sample_{product_type.replace('-', '_')}_{sequence:03d}"
    now = _iso(datetime.now(timezone.utc))
    document.update(
        {
            "_id": product_id,
            "productId": product_id,
            "sku": f"SMP-{product_type[:3].upper()}-{sequence:03d}",
            "productType": product_type,
            "name": f"Live Demo {product_type.title()} {sequence:03d}",
            "source": "live-sample",
            "schemaVersion": 2,
            "regionalTaxCode": "DE-STD",
            "marketAvailability": {"launchRegion": "DE", "visibleInDemo": True},
            "createdAt": now,
            "updatedAt": now,
        }
    )
    return document


SAMPLE_PRODUCTS_BY_TYPE = {product_type: build_live_sample(product_type, 1) for product_type in PRODUCT_TYPES}
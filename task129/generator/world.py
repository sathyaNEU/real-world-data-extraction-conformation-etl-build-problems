"""task129 generator: the fixed world. Device registry, release train, editions, people."""
from datetime import datetime, timedelta, date

import numpy as np
import pandas as pd

import params as P

# people, drawn with guard.py names --geo Denmark --seed 129 (listed on the card)
PEOPLE = {
    "requester": ("Elin Lauritsen", "head of digital operations"),
    "director": ("Ove Schmidt", "group digital director"),
    "frontend": ("Finn Thygesen", "front-end platform lead"),
    "editorial": ("Caroline Mortensen", "editorial product director"),
    "ads": ("Gunnar Paulsen", "head of ad operations"),
    "data": ("Gunhild Lund", "data engineer, digital operations"),
    "release": ("Mette Johansen", "release manager"),
    "perf": ("Simone Thorsen", "performance engineer"),
}

# ---------------------------------------------------------------- device registry
# (model string as the beacon reports it, brand, marketing name, form factor, os, year, score)
_MODELS = [
    ("SM-A057F", "Samsung", "Galaxy A05s", "phone", "Android", 2023, 412),
    ("SM-A145R", "Samsung", "Galaxy A14", "phone", "Android", 2023, 398),
    ("SM-A155F", "Samsung", "Galaxy A15", "phone", "Android", 2024, 455),
    ("SM-A146P", "Samsung", "Galaxy A14 5G", "phone", "Android", 2023, 471),
    ("moto g04", "Motorola", "moto g04", "phone", "Android", 2024, 366),
    ("moto e13", "Motorola", "moto e13", "phone", "Android", 2023, 241),
    ("23053RN02Y", "Xiaomi", "Redmi 12", "phone", "Android", 2023, 433),
    ("23108RN04Y", "Xiaomi", "Redmi 13C", "phone", "Android", 2023, 389),
    ("Nokia G21", "Nokia", "G21", "phone", "Android", 2022, 351),
    ("Nokia C32", "Nokia", "C32", "phone", "Android", 2023, 262),
    ("CPH2477", "OPPO", "A17", "phone", "Android", 2022, 372),
    ("RMX3710", "realme", "C55", "phone", "Android", 2023, 448),
    ("iPhone 8 class", "Apple", "iPhone 8 / SE (2nd gen)", "phone", "iOS", 2020, 489),
    ("SM-A256B", "Samsung", "Galaxy A25 5G", "phone", "Android", 2023, 702),
    ("SM-A356B", "Samsung", "Galaxy A35 5G", "phone", "Android", 2024, 788),
    ("SM-A546B", "Samsung", "Galaxy A54 5G", "phone", "Android", 2023, 811),
    ("SM-A556B", "Samsung", "Galaxy A55 5G", "phone", "Android", 2024, 893),
    ("Pixel 6a", "Google", "Pixel 6a", "phone", "Android", 2022, 905),
    ("Pixel 7a", "Google", "Pixel 7a", "phone", "Android", 2023, 951),
    ("moto g54 5G", "Motorola", "moto g54 5G", "phone", "Android", 2023, 690),
    ("moto g84 5G", "Motorola", "moto g84 5G", "phone", "Android", 2023, 744),
    ("23090RA98G", "Xiaomi", "Redmi Note 13 Pro 5G", "phone", "Android", 2024, 862),
    ("A142", "Nothing", "Phone (2a)", "phone", "Android", 2024, 917),
    ("iPhone 11 class", "Apple", "iPhone XR / 11", "phone", "iOS", 2019, 934),
    ("SM-S921B", "Samsung", "Galaxy S24", "phone", "Android", 2024, 1612),
    ("SM-S911B", "Samsung", "Galaxy S23", "phone", "Android", 2023, 1544),
    ("SM-S918B", "Samsung", "Galaxy S23 Ultra", "phone", "Android", 2023, 1588),
    ("Pixel 8", "Google", "Pixel 8", "phone", "Android", 2023, 1307),
    ("Pixel 8 Pro", "Google", "Pixel 8 Pro", "phone", "Android", 2023, 1341),
    ("Pixel 9", "Google", "Pixel 9", "phone", "Android", 2024, 1489),
    ("CPH2581", "OnePlus", "12", "phone", "Android", 2024, 1660),
    ("iPhone 13 class", "Apple", "iPhone 13 / 13 mini", "phone", "iOS", 2021, 1398),
    ("iPhone 14 class", "Apple", "iPhone 14 / 14 Plus", "phone", "iOS", 2022, 1452),
    ("iPhone 15 class", "Apple", "iPhone 15 / 15 Plus", "phone", "iOS", 2023, 1630),
    ("iPhone 15 Pro class", "Apple", "iPhone 15 Pro / Pro Max", "phone", "iOS", 2023, 1795),
    ("SM-X200", "Samsung", "Galaxy Tab A8", "tablet", "Android", 2022, 520),
    ("SM-X110", "Samsung", "Galaxy Tab A9", "tablet", "Android", 2023, 498),
    ("iPad 9 class", "Apple", "iPad (9th gen)", "tablet", "iOS", 2021, 1012),
    ("iPad Air class", "Apple", "iPad Air (5th gen)", "tablet", "iOS", 2022, 1660),
    ("TB-X606F", "Lenovo", "Tab M10 FHD Plus", "tablet", "Android", 2020, 402),
    # registry rows for models the sample never carries (the registry is the group's full list)
    ("SM-G991B", "Samsung", "Galaxy S21", "phone", "Android", 2021, 1188),
    ("Pixel 5", "Google", "Pixel 5", "phone", "Android", 2020, 652),
    ("moto g22", "Motorola", "moto g22", "phone", "Android", 2022, 301),
    ("SM-T290", "Samsung", "Galaxy Tab A 8.0", "tablet", "Android", 2019, 188),
]


def band(score):
    return "low" if score < 600 else ("mid" if score < 1000 else "high")


def registry():
    rows = []
    for m, b, name, ff, os_, yr, sc in _MODELS:
        rows.append({"device_model": m, "brand": b, "marketing_name": name, "form_factor": ff,
                     "os_family": os_, "release_year": yr, "cpu_benchmark": sc,
                     "perf_band": band(sc)})
    return pd.DataFrame(rows)


def models_by_class():
    reg = registry()
    seen = reg.iloc[:40]
    out = {}
    for c in ["low", "mid", "high"]:
        out[c] = seen[(seen.form_factor == "phone") & (seen.perf_band == c)].device_model.tolist()
    out["tablet"] = seen[seen.form_factor == "tablet"].device_model.tolist()
    return out


# ---------------------------------------------------------------- release train
def deploys(rng):
    """Deploy timestamps (local naive) from mid January to the end of August, about twice a week on
    irregular weekdays near 05:00, with the dated changes pinned to their release days."""
    pinned = {P.DATED["E"]: "E", P.DATED["B"]: "B", P.DATED["D"]: "D",
              P.PUZZLE_AD_SWITCH: "PUZ"}
    for c, d in P.COHORT_SWITCH.items():
        pinned[d] = "COH:" + c
    days = []
    d = date(2026, 1, 5)
    while d <= date(2026, 8, 31):
        days.append(d)
        step = int(rng.choice([2, 3, 3, 4, 5], p=[0.30, 0.30, 0.15, 0.15, 0.10]))
        d = d + timedelta(days=step)
        while d.weekday() >= 5:
            d = d + timedelta(days=1)
    days = sorted(set(days) | set(pinned))
    # drop days that crowd a pinned release (keep at least one clear day either side)
    keep = []
    for x in days:
        if x not in pinned and any(abs((x - p).days) <= 1 for p in pinned):
            continue
        keep.append(x)
    out = []
    for x in keep:
        minute = int(rng.integers(-18, 24))
        t = datetime(x.year, x.month, x.day, 5, 0) + timedelta(minutes=minute)
        out.append((t, pinned.get(x, "")))
    return out


def edition_register():
    rows = []
    for slug, (name, before, after) in P.EDITIONS.items():
        if after is None:
            rows.append({"edition_slug": slug, "edition_name": name, "masthead": before,
                         "valid_from": "2019-01-01", "valid_to": ""})
        else:
            rows.append({"edition_slug": slug, "edition_name": name, "masthead": before,
                         "valid_from": "2019-01-01", "valid_to": "2026-03-15"})
            rows.append({"edition_slug": slug, "edition_name": name, "masthead": after,
                         "valid_from": "2026-03-16", "valid_to": ""})
    return pd.DataFrame(rows)

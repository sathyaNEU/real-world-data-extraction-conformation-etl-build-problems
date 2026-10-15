"""The folder's two files the rating does not read: the producers' Subpart W greenhouse gas reports for their basin
facilities (2023 to 2025, calculated inventories) and a satellite product's monthly basin methane estimates."""
import json

import numpy as np

import world as W

SOURCES = [("Natural gas pneumatic device venting", 0.30), ("Atmospheric storage tanks", 0.17),
           ("Equipment leaks (population count)", 0.14), ("Liquids unloading", 0.07),
           ("Reciprocating compressor venting", 0.12), ("Associated gas venting and flaring", 0.08),
           ("Well testing venting and flaring", 0.02), ("Combustion equipment", 0.10)]


def ghgrp(seed, truth):
    """Each producer's reported CH4 by source, roughly a third to a half of what its sites emitted, for three years."""
    rng = np.random.default_rng(seed + 61)
    rows = []
    for k, p in enumerate(W.PRODUCERS):
        name = p[0]
        fid = 1_012_000 + 37 * k + int(rng.integers(0, 30))
        level = truth[name] * float(rng.uniform(0.32, 0.50))
        for y in (2023, 2024, 2025):
            tot = level * float(np.exp(rng.normal(0, 0.06))) * (1.04 if y == 2023 else 1.0)
            shares = np.array([s for _, s in SOURCES]) * np.exp(rng.normal(0, 0.15, len(SOURCES)))
            shares = shares / shares.sum()
            for (src, _), sh in zip(SOURCES, shares):
                ch4 = tot * sh
                rows.append(dict(year=y, fid=fid, fname="%s - %s Onshore Production" % (W.LEGAL[name], W.BASIN),
                                 parent=W.LEGAL[name], source=src, ch4=round(ch4, 2),
                                 co2e=round(ch4 * 25 + (ch4 * 9.0 if src == "Combustion equipment" else 0.0), 1)))
    return rows


def satellite(seed, basin_t):
    """A satellite product's monthly basin methane estimates with their 95 per cent ranges, wide enough to hold every
    reading of the producers' totals."""
    rng = np.random.default_rng(seed + 71)
    est = []
    months = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 10)]
    for (y, m) in months:
        mean = basin_t / 8760.0 * float(np.exp(rng.normal(0, 0.18)))
        est.append({"month": "%04d-%02d" % (y, m), "ch4_t_per_h": round(mean, 1),
                    "ci95_low": round(mean * float(rng.uniform(0.40, 0.48)), 1),
                    "ci95_high": round(mean * float(rng.uniform(1.45, 1.62)), 1),
                    "valid_overpasses": int(rng.integers(3, 12))})
    return {"product": "Basin methane flux, monthly (inversion of TROPOMI-class column data)",
            "basin": W.BASIN, "units": "t CH4 per hour", "version": "2.1", "released": "2026-10-28",
            "note": "Basin-wide totals; the product does not resolve individual facilities or operators.",
            "estimates": est}


def satellite_json(obj):
    return json.dumps(obj, indent=2) + "\n"

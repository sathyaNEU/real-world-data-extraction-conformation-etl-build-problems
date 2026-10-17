"""task193: generator/figures.json, every figure the write-up states."""
import json
import os


def write(here, g):
    obj = {
        "referred_count": g["referred_count"],
        "crude_count": g["crude_count"],
        "rung0_count": g["rung0_count"],
        "candidate_count": g["candidate_count"],
        "screened_count": g["screened_count"],
        "patients_in_extract": g["patients_in_extract"],
        "referred": g["referred"],
        "crude_only": g["crude_only"],
        "window_only": g["window_only"],
        "nearest_miss": g["nearest_miss"],
        "screen_rows": g["screen_rows"],
        "chart_rows": g["chart_rows"],
        "a1": g["a1"],
        "a2": g["a2"],
        "a3": g["a3"],
        "routes": {k: len(v) for k, v in g["routes"].items()},
        "standard_sections": g["standard_sections"],
        "referral_multiple": 1.25,
        "referral_year": 2027,
        "rung2_count": g["rung2_count"],
        "crude_only_count": len(g["crude_only"]),
        "window_only_count": len(g["window_only"]),
    }
    with open(os.path.join(here, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=True)
        fh.write("\n")

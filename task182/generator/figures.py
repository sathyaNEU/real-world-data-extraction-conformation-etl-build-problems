"""Write generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    rows = {r["position"]: r for r in g["rows"]}
    out = {
        "call": "the October slot covers " + ", ".join(g["slate_ordered"]),
        "slate": g["slate"],
        "slate_ordered": g["slate_ordered"],
        "slate_dwellings": {c: d for c, d, _, _ in g["slate_dwellings"]},
        "sixth": g["sixth"],
        "sixth_dwelling": g["sixth_dwelling"],
        "sixth_level_db": g["sixth_level"],
        "margin_db": g["margin_db"],
        "cap": g["cap"],
        "specific_level_db": {c: rows[c]["specific_db"] for c in sorted(rows)},
        "measured_total_db": {c: rows[c]["total_db"] for c in sorted(rows)},
        "residual_db": {c: rows[c]["residual_db"] for c in sorted(rows)},
        "valid_minutes": {c: rows[c]["valid_minutes"] for c in sorted(rows)},
        "excluded_minutes": {c: rows[c]["excluded_minutes"] for c in sorted(rows)},
        "stop_minutes": {c: rows[c]["stop_minutes"] for c in sorted(rows)},
        "highest_band_hz": {c: (rows[c]["band_hz"] if rows[c]["band_hz"] else "none") for c in sorted(rows)},
        "tone_prominent": {c: ("none" if rows[c]["tone"] is None else ("yes" if rows[c]["tone"] else "no"))
                           for c in sorted(rows)},
        "weekly_plant": {str(k): v for k, v in sorted(g["weekly"].items())},
        "rungs": {k: {"slate": v[0], "margin_db": v[1], "next": v[2]} for k, v in g["slates"].items()},
        "plan_clauses": ["2.1", "2.2", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "5.1", "6.1"],
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p

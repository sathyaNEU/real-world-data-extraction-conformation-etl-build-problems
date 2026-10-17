"""Write generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    out = {
        "call": g["fund"],
        "decided_port": g["decided_port"],
        "decided_shortfall_kbps": int(g["decided_shortfall"]),
        "decided_evening": g["decided_evening"],
        "decided_window": g["decided_window"],
        "closest_port": g["closest_port"],
        "closest_shortfall_kbps": int(g["closest_shortfall"]),
        "flip_shortfall_kbps": int(g["record_shortfall"]),
        "flip_quarter": g["record_quarter"],
        "rank_of_nine": g["rank_of_nine"],
        "quarterly_worst_kbps": g["quarterly_worst"],
        "grid": {"%s %s" % (l, w): {"worst_kbps": v[0], "evening": v[1]}
                 for (l, w), v in sorted(g["grid"].items())},
        "rung0_port": g["rung0_port"],
        "rung0_shortfall_kbps": int(g["rung0_shortfall"]),
        "rung2_port": g["rung2_port"],
        "rung2_mean_kbps": round(g["rung2_mean"], 1),
        "rung2_next_kbps": round(g["rung2_next"], 1),
        "own_99th_kbps": {k: int(round(v)) for k, v in g["own_99th"].items()},
        "framework_clauses": ["4.1", "4.2", "4.3", "4.4", "4.5", "5.1", "7.1", "7.2"],
        "evenings_in_quarter": g["evenings_in_quarter"],
        "evenings_left_out": g["evenings_left_out"],
        "windows_assessed": g["windows_assessed"],
        "windows_in_quarter": g["windows_in_quarter"],
        "record_windows": g["record_windows"],
        "record_windows_at_or_above": g["record_windows_at_or_above"],
        "closest_over_own_99th_pct": g["closest_over_own_99th_pct"],
        "closest_below_record_pct": g["closest_below_record_pct"],
        "a1_peers": g["a1_peers"],
        "a2_builds": g["a2_builds"],
        "a3_incidents": g["a3_incidents"],
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p
